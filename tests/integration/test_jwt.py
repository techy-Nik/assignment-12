import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import jwt, JWTError
from uuid import uuid4, UUID
import secrets

# Configure to only use asyncio backend, not trio
pytestmark = pytest.mark.anyio

from app.auth.jwt import (
    verify_password,
    get_password_hash,
    create_token,
    decode_token,
    get_current_user,
    pwd_context
)
from app.schemas.token import TokenType
from app.models.user import User
from app.core.config import get_settings

settings = get_settings()


# ==================== Password Hashing Tests ====================

def test_get_password_hash():
    """Test password hashing"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert hashed.startswith("$2b$")  # bcrypt hash format
    assert len(hashed) > 50


def test_verify_password_correct():
    """Test password verification with correct password"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password"""
    password = "testpassword123"
    wrong_password = "wrongpassword"
    hashed = get_password_hash(password)
    
    assert verify_password(wrong_password, hashed) is False


# ==================== Token Creation Tests ====================

def test_create_token_access_default_expiry():
    """Test creating access token with default expiry (line 46 - if branch)"""
    user_id = uuid4()
    
    token = create_token(user_id, TokenType.ACCESS)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode to verify contents
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert payload["sub"] == str(user_id)
    assert payload["type"] == TokenType.ACCESS.value
    assert "exp" in payload
    assert "iat" in payload
    assert "jti" in payload


def test_create_token_refresh_default_expiry():
    """Test creating refresh token with default expiry (line 46 - else branch)"""
    user_id = uuid4()
    
    token = create_token(user_id, TokenType.REFRESH)
    
    assert isinstance(token, str)
    
    # Decode to verify contents
    payload = jwt.decode(
        token,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert payload["sub"] == str(user_id)
    assert payload["type"] == TokenType.REFRESH.value


def test_create_token_custom_expiry():
    """Test creating token with custom expiry (line 46 - if expires_delta)"""
    user_id = uuid4()
    custom_delta = timedelta(minutes=30)
    
    token = create_token(user_id, TokenType.ACCESS, expires_delta=custom_delta)
    
    assert isinstance(token, str)
    
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    # Verify expiry is approximately 30 minutes from now
    exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    expected_time = datetime.now(timezone.utc) + custom_delta
    
    # Allow 2 second tolerance
    assert abs((exp_time - expected_time).total_seconds()) < 2


def test_create_token_string_user_id():
    """Test creating token with string user_id (line 58)"""
    user_id = str(uuid4())
    
    token = create_token(user_id, TokenType.ACCESS)
    
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert payload["sub"] == user_id


def test_create_token_uuid_user_id():
    """Test creating token with UUID user_id (line 58)"""
    user_id = uuid4()
    
    token = create_token(user_id, TokenType.ACCESS)
    
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert payload["sub"] == str(user_id)


def test_create_token_exception_handling():
    """Test token creation error handling (lines 76-77)"""
    with patch('app.auth.jwt.jwt.encode', side_effect=Exception("Encoding error")):
        with pytest.raises(HTTPException) as exc_info:
            create_token(uuid4(), TokenType.ACCESS)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Could not create token" in exc_info.value.detail


# ==================== Token Decoding Tests ====================

async def test_decode_token_valid_access_token():
    """Test decoding valid access token (lines 90-104)"""
    user_id = uuid4()
    token = create_token(user_id, TokenType.ACCESS)
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        payload = await decode_token(token, TokenType.ACCESS)
    
    assert payload["sub"] == str(user_id)
    assert payload["type"] == TokenType.ACCESS.value
    assert "jti" in payload


async def test_decode_token_valid_refresh_token():
    """Test decoding valid refresh token (lines 90-104)"""
    user_id = uuid4()
    token = create_token(user_id, TokenType.REFRESH)
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        payload = await decode_token(token, TokenType.REFRESH)
    
    assert payload["sub"] == str(user_id)
    assert payload["type"] == TokenType.REFRESH.value


async def test_decode_token_wrong_token_type():
    """Test decoding token with wrong type (lines 105-110)"""
    user_id = uuid4()
    token = create_token(user_id, TokenType.ACCESS)
    
    # Mock jwt.decode to return payload with wrong type
    with patch('app.auth.jwt.jwt.decode') as mock_decode:
        mock_decode.return_value = {
            "sub": str(user_id),
            "type": TokenType.ACCESS.value,  # ACCESS type but we're checking for REFRESH
            "jti": "test_jti"
        }
        with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await decode_token(token, TokenType.REFRESH)
            
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "Invalid token type"


async def test_decode_token_blacklisted():
    """Test decoding blacklisted token (lines 112-117)"""
    user_id = uuid4()
    token = create_token(user_id, TokenType.ACCESS)
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=True):
        with pytest.raises(HTTPException) as exc_info:
            await decode_token(token, TokenType.ACCESS)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Token has been revoked"


async def test_decode_token_expired():
    """Test decoding expired token (lines 121-126)"""
    user_id = uuid4()
    # Create token that expired 1 hour ago
    expired_token = create_token(
        user_id,
        TokenType.ACCESS,
        expires_delta=timedelta(hours=-1)
    )
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await decode_token(expired_token, TokenType.ACCESS)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Token has expired"


async def test_decode_token_invalid_jwt():
    """Test decoding invalid JWT (lines 127)"""
    invalid_token = "invalid.jwt.token"
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await decode_token(invalid_token, TokenType.ACCESS)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Could not validate credentials"


async def test_decode_token_with_verify_exp_false():
    """Test decoding token without expiry verification"""
    user_id = uuid4()
    # Create expired token
    expired_token = create_token(
        user_id,
        TokenType.ACCESS,
        expires_delta=timedelta(hours=-1)
    )
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        # Should not raise exception when verify_exp=False
        payload = await decode_token(expired_token, TokenType.ACCESS, verify_exp=False)
        assert payload["sub"] == str(user_id)


# ==================== Get Current User Tests ====================

@pytest.fixture
def mock_db():
    """Mock database session"""
    return MagicMock()


@pytest.fixture
def sample_user():
    """Sample user for testing"""
    user = User()
    user.id = uuid4()
    user.username = "testuser"
    user.email = "test@example.com"
    user.is_active = True
    user.is_verified = True
    return user


async def test_get_current_user_success(mock_db, sample_user):
    """Test successful user retrieval (lines 141-161)"""
    user_id = sample_user.id
    token = create_token(user_id, TokenType.ACCESS)
    
    # Mock database query
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = sample_user
    mock_db.query.return_value = mock_query
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        user = await get_current_user(token=token, db=mock_db)
    
    assert user == sample_user
    assert user.id == user_id
    assert user.is_active is True


async def test_get_current_user_not_found(mock_db):
    """Test user not found in database (lines 148-152)
    
    Note: The exception handler catches the HTTPException and re-raises it as 401
    """
    user_id = uuid4()
    token = create_token(user_id, TokenType.ACCESS)
    
    # Mock database query returning None
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=token, db=mock_db)
        
        # The exception handler in get_current_user catches and converts to 401
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_current_user_inactive(mock_db, sample_user):
    """Test inactive user (lines 154-158)
    
    Note: The exception handler catches the HTTPException and re-raises it as 401
    """
    sample_user.is_active = False
    user_id = sample_user.id
    token = create_token(user_id, TokenType.ACCESS)
    
    # Mock database query
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = sample_user
    mock_db.query.return_value = mock_query
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=token, db=mock_db)
        
        # The exception handler in get_current_user catches and converts to 401
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_current_user_invalid_token(mock_db):
    """Test with invalid token (lines 160-161)"""
    invalid_token = "invalid.jwt.token"
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=invalid_token, db=mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_current_user_expired_token(mock_db):
    """Test with expired token"""
    user_id = uuid4()
    expired_token = create_token(
        user_id,
        TokenType.ACCESS,
        expires_delta=timedelta(hours=-1)
    )
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=expired_token, db=mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_current_user_blacklisted_token(mock_db):
    """Test with blacklisted token"""
    user_id = uuid4()
    token = create_token(user_id, TokenType.ACCESS)
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=True):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=token, db=mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        # Check that the detail message is in the error string
        assert "Token has been revoked" in str(exc_info.value.detail)


async def test_get_current_user_database_exception(mock_db, sample_user):
    """Test database exception handling (lines 160-161)"""
    user_id = sample_user.id
    token = create_token(user_id, TokenType.ACCESS)
    
    # Mock database query to raise exception
    mock_db.query.side_effect = Exception("Database connection error")
    
    with patch('app.auth.jwt.is_blacklisted', new_callable=AsyncMock, return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=token, db=mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED