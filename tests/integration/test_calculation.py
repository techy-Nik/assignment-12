import pytest
import uuid

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    AbstractCalculation,
)

# Helper function to create a dummy user_id for testing.
def dummy_user_id():
    return uuid.uuid4()

# ======================================================================================
# Addition Tests
# ======================================================================================

def test_addition_get_result():
    """
    Test that Addition.get_result returns the correct sum.
    """
    inputs = [10, 5, 3.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"


def test_addition_with_two_numbers():
    """
    Test addition with exactly two numbers.
    """
    inputs = [7.5, 2.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == 10.0


def test_addition_with_negative_numbers():
    """
    Test addition with negative numbers.
    """
    inputs = [10, -5, 3]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == 8


def test_invalid_inputs_for_addition_not_list():
    """
    Test that providing non-list inputs to Addition.get_result raises a ValueError (line 116).
    """
    addition = Addition(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()


def test_invalid_inputs_for_addition_dict():
    """
    Test that providing dict inputs to Addition.get_result raises a ValueError (line 116).
    """
    addition = Addition(user_id=dummy_user_id(), inputs={"a": 1, "b": 2})
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()


def test_invalid_inputs_for_addition_too_few():
    """
    Test that providing fewer than two numbers to Addition.get_result raises a ValueError.
    """
    addition = Addition(user_id=dummy_user_id(), inputs=[5])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        addition.get_result()


def test_invalid_inputs_for_addition_empty():
    """
    Test that providing an empty list to Addition.get_result raises a ValueError.
    """
    addition = Addition(user_id=dummy_user_id(), inputs=[])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        addition.get_result()


# ======================================================================================
# Subtraction Tests
# ======================================================================================

def test_subtraction_get_result():
    """
    Test that Subtraction.get_result returns the correct difference.
    """
    inputs = [20, 5, 3]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    # Expected: 20 - 5 - 3 = 12
    result = subtraction.get_result()
    assert result == 12, f"Expected 12, got {result}"


def test_subtraction_with_two_numbers():
    """
    Test subtraction with exactly two numbers.
    """
    inputs = [15, 7]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    result = subtraction.get_result()
    assert result == 8


def test_subtraction_with_negative_result():
    """
    Test subtraction that results in a negative number.
    """
    inputs = [5, 10]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    result = subtraction.get_result()
    assert result == -5


def test_invalid_inputs_for_subtraction_not_list():
    """
    Test that providing non-list inputs to Subtraction.get_result raises a ValueError (line 125).
    """
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=42)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        subtraction.get_result()


def test_invalid_inputs_for_subtraction_string():
    """
    Test that providing string inputs to Subtraction.get_result raises a ValueError (line 125).
    """
    subtraction = Subtraction(user_id=dummy_user_id(), inputs="10-5")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        subtraction.get_result()


def test_invalid_inputs_for_subtraction_too_few():
    """
    Test that providing fewer than two numbers to Subtraction.get_result raises a ValueError.
    """
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        subtraction.get_result()


# ======================================================================================
# Multiplication Tests
# ======================================================================================

def test_multiplication_get_result():
    """
    Test that Multiplication.get_result returns the correct product.
    """
    inputs = [2, 3, 4]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 24, f"Expected 24, got {result}"


def test_multiplication_with_two_numbers():
    """
    Test multiplication with exactly two numbers.
    """
    inputs = [6, 7]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 42


def test_multiplication_with_zero():
    """
    Test multiplication with zero.
    """
    inputs = [5, 0, 3]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 0


def test_invalid_inputs_for_multiplication_not_list():
    """
    Test that providing non-list inputs to Multiplication.get_result raises a ValueError (line 139).
    """
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=100)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        multiplication.get_result()


def test_invalid_inputs_for_multiplication_tuple():
    """
    Test that providing tuple inputs to Multiplication.get_result raises a ValueError (line 139).
    """
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=(2, 3, 4))
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        multiplication.get_result()


def test_invalid_inputs_for_multiplication_too_few():
    """
    Test that providing fewer than two numbers to Multiplication.get_result raises a ValueError (line 141).
    """
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=[5])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        multiplication.get_result()


def test_invalid_inputs_for_multiplication_empty():
    """
    Test that providing an empty list to Multiplication.get_result raises a ValueError (line 141).
    """
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=[])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        multiplication.get_result()


# ======================================================================================
# Division Tests
# ======================================================================================

def test_division_get_result():
    """
    Test that Division.get_result returns the correct quotient.
    """
    inputs = [100, 2, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    # Expected: 100 / 2 / 5 = 10
    result = division.get_result()
    assert result == 10, f"Expected 10, got {result}"


def test_division_with_two_numbers():
    """
    Test division with exactly two numbers.
    """
    inputs = [50, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    result = division.get_result()
    assert result == 10


def test_division_with_decimals():
    """
    Test division resulting in decimal.
    """
    inputs = [10, 4]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    result = division.get_result()
    assert result == 2.5


def test_division_by_zero():
    """
    Test that Division.get_result raises ValueError when dividing by zero.
    """
    inputs = [50, 0, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


def test_division_by_zero_in_middle():
    """
    Test that Division.get_result raises ValueError when zero appears in the middle.
    """
    inputs = [100, 2, 0, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


def test_invalid_inputs_for_division_not_list():
    """
    Test that providing non-list inputs to Division.get_result raises a ValueError (line 153).
    """
    division = Division(user_id=dummy_user_id(), inputs=None)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        division.get_result()


def test_invalid_inputs_for_division_set():
    """
    Test that providing set inputs to Division.get_result raises a ValueError (line 153).
    """
    division = Division(user_id=dummy_user_id(), inputs={10, 2})
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        division.get_result()


def test_invalid_inputs_for_division_too_few():
    """
    Test that providing fewer than two numbers to Division.get_result raises a ValueError.
    """
    division = Division(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        division.get_result()


# ======================================================================================
# Factory Method Tests
# ======================================================================================

def test_calculation_factory_addition():
    """
    Test the Calculation.create factory method for addition.
    """
    inputs = [1, 2, 3]
    calc = Calculation.create(
        calculation_type='addition',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Check that the returned instance is an Addition.
    assert isinstance(calc, Addition), "Factory did not return an Addition instance."
    assert calc.get_result() == sum(inputs), "Incorrect addition result."


def test_calculation_factory_subtraction():
    """
    Test the Calculation.create factory method for subtraction.
    """
    inputs = [10, 4]
    calc = Calculation.create(
        calculation_type='subtraction',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 10 - 4 = 6
    assert isinstance(calc, Subtraction), "Factory did not return a Subtraction instance."
    assert calc.get_result() == 6, "Incorrect subtraction result."


def test_calculation_factory_multiplication():
    """
    Test the Calculation.create factory method for multiplication.
    """
    inputs = [3, 4, 2]
    calc = Calculation.create(
        calculation_type='multiplication',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 3 * 4 * 2 = 24
    assert isinstance(calc, Multiplication), "Factory did not return a Multiplication instance."
    assert calc.get_result() == 24, "Incorrect multiplication result."


def test_calculation_factory_division():
    """
    Test the Calculation.create factory method for division.
    """
    inputs = [100, 2, 5]
    calc = Calculation.create(
        calculation_type='division',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    # Expected: 100 / 2 / 5 = 10
    assert isinstance(calc, Division), "Factory did not return a Division instance."
    assert calc.get_result() == 10, "Incorrect division result."


def test_calculation_factory_case_insensitive():
    """
    Test that the factory method handles case-insensitive calculation types.
    """
    inputs = [10, 5]
    calc_upper = Calculation.create(
        calculation_type='ADDITION',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    calc_mixed = Calculation.create(
        calculation_type='AdDiTiOn',
        user_id=dummy_user_id(),
        inputs=inputs,
    )
    assert isinstance(calc_upper, Addition)
    assert isinstance(calc_mixed, Addition)


def test_calculation_factory_invalid_type():
    """
    Test that Calculation.create raises a ValueError for an unsupported calculation type.
    """
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type='modulus',  # unsupported type
            user_id=dummy_user_id(),
            inputs=[10, 3],
        )


def test_calculation_factory_empty_string():
    """
    Test that Calculation.create raises a ValueError for empty string type.
    """
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(
            calculation_type='',
            user_id=dummy_user_id(),
            inputs=[10, 3],
        )


def test_calculation_factory_none_type():
    """
    Test that Calculation.create handles None type gracefully.
    """
    with pytest.raises(AttributeError):  # None has no .lower() method
        Calculation.create(
            calculation_type=None,
            user_id=dummy_user_id(),
            inputs=[10, 3],
        )


# ======================================================================================
# Abstract Class Tests
# ======================================================================================

def test_calculation_base_get_result_not_implemented():
    """
    Test that calling get_result on the base Calculation raises NotImplementedError (line 95).
    """
    # Create a base Calculation instance (not a subclass)
    calc = Calculation(user_id=dummy_user_id(), type="base", inputs=[1, 2])
    
    with pytest.raises(NotImplementedError):
        calc.get_result()


def test_calculation_repr():
    """
    Test the __repr__ method of calculations (line 98).
    """
    inputs = [10, 5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    
    repr_str = repr(addition)
    
    assert "Calculation" in repr_str
    assert "type=" in repr_str
    assert "inputs=" in repr_str
    assert str(inputs) in repr_str


def test_calculation_repr_with_different_types():
    """
    Test __repr__ for different calculation types.
    """
    user_id = dummy_user_id()
    inputs = [20, 4]
    
    subtraction = Subtraction(user_id=user_id, inputs=inputs)
    multiplication = Multiplication(user_id=user_id, inputs=inputs)
    division = Division(user_id=user_id, inputs=inputs)
    
    assert "subtraction" in repr(subtraction)
    assert "multiplication" in repr(multiplication)
    assert "division" in repr(division)


# ======================================================================================
# Edge Cases and Additional Coverage
# ======================================================================================

def test_calculation_with_float_inputs():
    """
    Test calculations with floating point inputs.
    """
    inputs = [3.5, 2.5, 1.0]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    assert addition.get_result() == 7.0


def test_calculation_with_large_numbers():
    """
    Test calculations with large numbers.
    """
    inputs = [1000000, 2000000, 3000000]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    assert addition.get_result() == 6000000


def test_calculation_with_many_inputs():
    """
    Test calculations with many inputs.
    """
    inputs = list(range(1, 11))  # [1, 2, 3, ..., 10]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    assert addition.get_result() == 55  # sum of 1 to 10