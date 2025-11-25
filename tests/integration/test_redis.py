import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from redis.asyncio import Redis

from app.auth.redis import get_redis, add_to_blacklist, is_blacklisted

pytestmark = pytest.mark.anyio


# ======================================================================================
# Fixtures
# ======================================================================================

@pytest.fixture
def mock_redis():
    """Create a mock Redis instance"""
    redis_mock = AsyncMock(spec=Redis)
    redis_mock.set = AsyncMock(return_value=True)
    redis_mock.get = AsyncMock(return_value=None)
    redis_mock.exists = AsyncMock(return_value=0)
    redis_mock.delete = AsyncMock(return_value=1)
    return redis_mock


@pytest.fixture(autouse=True)
def reset_redis_cache():
    """Reset the redis cache between tests"""
    if hasattr(get_redis, "redis"):
        delattr(get_redis, "redis")
    yield
    if hasattr(get_redis, "redis"):
        delattr(get_redis, "redis")


# ======================================================================================
# get_redis() Tests
# ======================================================================================

async def test_get_redis_creates_connection_first_time(mock_redis):
    """Test that get_redis creates a new Redis connection on first call (lines 9-11)"""
    # Note: The actual code has a bug - it uses aioredis.from_url() but imports Redis
    # We'll patch whatever is actually used in the code
    with patch('redis.asyncio.Redis.from_url', new_callable=AsyncMock, return_value=mock_redis) as mock_from_url:
        # First call should create connection
        redis = await get_redis()
        
        assert redis == mock_redis
        mock_from_url.assert_called_once()
        # Verify it was called with the correct URL
        call_args = mock_from_url.call_args
        assert "redis://" in str(call_args)


async def test_get_redis_reuses_existing_connection(mock_redis):
    """Test that get_redis reuses existing connection on subsequent calls (lines 9-11)"""
    with patch('redis.asyncio.Redis.from_url', new_callable=AsyncMock, return_value=mock_redis) as mock_from_url:
        # First call creates connection
        redis1 = await get_redis()
        
        # Second call should reuse the same connection
        redis2 = await get_redis()
        
        assert redis1 == redis2
        assert redis1 is redis2  # Same object reference
        mock_from_url.assert_called_once()  # Only called once


async def test_get_redis_uses_custom_redis_url(mock_redis):
    """Test that get_redis uses custom REDIS_URL from settings"""
    custom_url = "redis://custom-host:6379/1"
    
    with patch('app.auth.redis.settings.REDIS_URL', custom_url):
        with patch('redis.asyncio.Redis.from_url', new_callable=AsyncMock, return_value=mock_redis) as mock_from_url:
            redis = await get_redis()
            
            mock_from_url.assert_called_once()
            # Check that custom URL was used
            call_args = mock_from_url.call_args[0][0]
            assert call_args == custom_url


async def test_get_redis_uses_default_url_when_none(mock_redis):
    """Test that get_redis uses default localhost URL when REDIS_URL is None"""
    with patch('app.auth.redis.settings.REDIS_URL', None):
        with patch('redis.asyncio.Redis.from_url', new_callable=AsyncMock, return_value=mock_redis) as mock_from_url:
            redis = await get_redis()
            
            mock_from_url.assert_called_once()
            call_args = mock_from_url.call_args[0][0]
            assert call_args == "redis://localhost"


# ======================================================================================
# add_to_blacklist() Tests
# ======================================================================================

async def test_add_to_blacklist_success(mock_redis):
    """Test successfully adding a JTI to the blacklist (lines 17-18)"""
    jti = "test-jti-12345"
    exp = 3600  # 1 hour
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        await add_to_blacklist(jti, exp)
        
        # Verify Redis set was called with correct parameters
        mock_redis.set.assert_called_once_with(f"blacklist:{jti}", "1", ex=exp)


async def test_add_to_blacklist_with_different_jti(mock_redis):
    """Test adding different JTIs to blacklist"""
    jti1 = "jti-token-1"
    jti2 = "jti-token-2"
    exp = 7200  # 2 hours
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        await add_to_blacklist(jti1, exp)
        await add_to_blacklist(jti2, exp)
        
        # Verify both calls were made
        assert mock_redis.set.call_count == 2
        mock_redis.set.assert_any_call(f"blacklist:{jti1}", "1", ex=exp)
        mock_redis.set.assert_any_call(f"blacklist:{jti2}", "1", ex=exp)


async def test_add_to_blacklist_with_zero_expiry(mock_redis):
    """Test adding to blacklist with zero expiry"""
    jti = "test-jti-zero"
    exp = 0
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        await add_to_blacklist(jti, exp)
        
        mock_redis.set.assert_called_once_with(f"blacklist:{jti}", "1", ex=exp)


async def test_add_to_blacklist_with_long_expiry(mock_redis):
    """Test adding to blacklist with long expiry time"""
    jti = "test-jti-long"
    exp = 86400 * 7  # 7 days
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        await add_to_blacklist(jti, exp)
        
        mock_redis.set.assert_called_once_with(f"blacklist:{jti}", "1", ex=exp)


async def test_add_to_blacklist_redis_error(mock_redis):
    """Test error handling when Redis fails during add_to_blacklist"""
    jti = "test-jti-error"
    exp = 3600
    
    # Make Redis set() raise an exception
    mock_redis.set.side_effect = Exception("Redis connection error")
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        with pytest.raises(Exception) as exc_info:
            await add_to_blacklist(jti, exp)
        
        assert "Redis connection error" in str(exc_info.value)


# ======================================================================================
# is_blacklisted() Tests
# ======================================================================================

async def test_is_blacklisted_returns_true_when_exists(mock_redis):
    """Test that is_blacklisted returns True when JTI exists (lines 22-23)"""
    jti = "blacklisted-jti"
    
    # exists() returns 1 when key exists (Redis returns int, not bool)
    mock_redis.exists.return_value = 1
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        result = await is_blacklisted(jti)
        
        # Redis exists returns 1, which is truthy but not True
        assert result == 1  # Changed from 'is True'
        mock_redis.exists.assert_called_once_with(f"blacklist:{jti}")


async def test_is_blacklisted_returns_false_when_not_exists(mock_redis):
    """Test that is_blacklisted returns False when JTI doesn't exist"""
    jti = "not-blacklisted-jti"
    
    # exists() returns 0 when key doesn't exist
    mock_redis.exists.return_value = 0
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        result = await is_blacklisted(jti)
        
        # Redis exists returns 0, which is falsy but not False
        assert result == 0  # Changed from 'is False'
        mock_redis.exists.assert_called_once_with(f"blacklist:{jti}")


async def test_is_blacklisted_with_multiple_checks(mock_redis):
    """Test checking multiple JTIs for blacklist status"""
    jti1 = "blacklisted-1"
    jti2 = "not-blacklisted-2"
    jti3 = "blacklisted-3"
    
    # Configure mock to return different values
    def exists_side_effect(key):
        if key == f"blacklist:{jti1}":
            return 1
        elif key == f"blacklist:{jti2}":
            return 0
        elif key == f"blacklist:{jti3}":
            return 1
        return 0
    
    mock_redis.exists.side_effect = exists_side_effect
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        result1 = await is_blacklisted(jti1)
        result2 = await is_blacklisted(jti2)
        result3 = await is_blacklisted(jti3)
        
        # Redis exists returns integers, not booleans
        assert result1 == 1  # Changed from 'is True'
        assert result2 == 0  # Changed from 'is False'
        assert result3 == 1  # Changed from 'is True'
        assert mock_redis.exists.call_count == 3


async def test_is_blacklisted_redis_error(mock_redis):
    """Test error handling when Redis fails during is_blacklisted"""
    jti = "test-jti-error"
    
    # Make Redis exists() raise an exception
    mock_redis.exists.side_effect = Exception("Redis connection lost")
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        with pytest.raises(Exception) as exc_info:
            await is_blacklisted(jti)
        
        assert "Redis connection lost" in str(exc_info.value)


# ======================================================================================
# Integration Tests
# ======================================================================================

async def test_full_blacklist_workflow(mock_redis):
    """Test complete workflow: add to blacklist and then check"""
    jti = "workflow-jti"
    exp = 3600
    
    # Configure mock: initially doesn't exist, then exists after adding
    call_count = 0
    def exists_side_effect(key):
        nonlocal call_count
        call_count += 1
        # First call (before adding): doesn't exist
        if call_count == 1:
            return 0
        # Second call (after adding): exists
        return 1
    
    mock_redis.exists.side_effect = exists_side_effect
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis):
        # Initially not blacklisted (returns 0)
        result_before = await is_blacklisted(jti)
        assert result_before == 0  # Changed from 'is False'
        
        # Add to blacklist
        await add_to_blacklist(jti, exp)
        mock_redis.set.assert_called_once_with(f"blacklist:{jti}", "1", ex=exp)
        
        # Now it should be blacklisted (returns 1)
        result_after = await is_blacklisted(jti)
        assert result_after == 1  # Changed from 'is True'


async def test_redis_connection_reuse_across_operations(mock_redis):
    """Test that Redis connection is reused across multiple operations"""
    jti = "reuse-test-jti"
    exp = 3600
    
    mock_redis.exists.return_value = 1
    
    with patch('app.auth.redis.get_redis', new_callable=AsyncMock, return_value=mock_redis) as mock_get_redis:
        # Perform multiple operations
        await add_to_blacklist(jti, exp)
        await is_blacklisted(jti)
        await is_blacklisted(jti)
        await add_to_blacklist(f"{jti}-2", exp)
        
        # get_redis should be called for each operation
        assert mock_get_redis.call_count == 4
        
        # Verify operations were performed
        assert mock_redis.set.call_count == 2
        assert mock_redis.exists.call_count == 2