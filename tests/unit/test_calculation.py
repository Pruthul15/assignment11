"""
Unit tests for Calculation models.
Tests polymorphic inheritance, factory pattern, and calculation logic.
Author: Pruthul Patel
Date: October 18, 2025
"""
import pytest
import uuid
from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division
)


class TestCalculationFactory:
    """Test the factory pattern for creating calculations"""
    
    def test_create_addition(self):
        """Test creating an addition calculation"""
        user_id = uuid.uuid4()
        calc = Calculation.create('addition', user_id, [1.0, 2.0, 3.0])
        assert isinstance(calc, Addition)
        assert calc.type == 'addition'
        assert calc.inputs == [1.0, 2.0, 3.0]
    
    def test_create_subtraction(self):
        """Test creating a subtraction calculation"""
        user_id = uuid.uuid4()
        calc = Calculation.create('subtraction', user_id, [10.0, 5.0])
        assert isinstance(calc, Subtraction)
        assert calc.type == 'subtraction'
    
    def test_create_multiplication(self):
        """Test creating a multiplication calculation"""
        user_id = uuid.uuid4()
        calc = Calculation.create('multiplication', user_id, [2.0, 3.0, 4.0])
        assert isinstance(calc, Multiplication)
        assert calc.type == 'multiplication'
    
    def test_create_division(self):
        """Test creating a division calculation"""
        user_id = uuid.uuid4()
        calc = Calculation.create('division', user_id, [12.0, 3.0])
        assert isinstance(calc, Division)
        assert calc.type == 'division'
    
    def test_create_invalid_type(self):
        """Test creating calculation with invalid type raises error"""
        user_id = uuid.uuid4()
        with pytest.raises(ValueError, match="Unsupported calculation type"):
            Calculation.create('invalid_type', user_id, [1.0, 2.0])
    
    def test_create_case_insensitive(self):
        """Test factory method is case insensitive"""
        user_id = uuid.uuid4()
        calc1 = Calculation.create('ADDITION', user_id, [1.0, 2.0])
        calc2 = Calculation.create('Addition', user_id, [1.0, 2.0])
        calc3 = Calculation.create('addition', user_id, [1.0, 2.0])
        assert all(isinstance(c, Addition) for c in [calc1, calc2, calc3])


class TestAddition:
    """Test Addition calculation logic"""
    
    def test_addition_two_numbers(self):
        """Test adding two numbers"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[5.0, 3.0])
        assert calc.get_result() == 8.0
    
    def test_addition_multiple_numbers(self):
        """Test adding multiple numbers"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[1.0, 2.0, 3.0, 4.0])
        assert calc.get_result() == 10.0
    
    def test_addition_negative_numbers(self):
        """Test adding negative numbers"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[-5.0, 3.0])
        assert calc.get_result() == -2.0
    
    def test_addition_decimals(self):
        """Test adding decimal numbers"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[1.5, 2.3, 3.7])
        assert calc.get_result() == pytest.approx(7.5)
    
    def test_addition_invalid_inputs_not_list(self):
        """Test addition with non-list inputs raises error"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs="not a list")
        with pytest.raises(ValueError, match="Inputs must be a list"):
            calc.get_result()
    
    def test_addition_insufficient_inputs(self):
        """Test addition with less than 2 numbers raises error"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[1.0])
        with pytest.raises(ValueError, match="at least two numbers"):
            calc.get_result()


class TestSubtraction:
    """Test Subtraction calculation logic"""
    
    def test_subtraction_two_numbers(self):
        """Test subtracting two numbers"""
        user_id = uuid.uuid4()
        calc = Subtraction(user_id=user_id, inputs=[10.0, 3.0])
        assert calc.get_result() == 7.0
    
    def test_subtraction_multiple_numbers(self):
        """Test subtracting multiple numbers sequentially"""
        user_id = uuid.uuid4()
        calc = Subtraction(user_id=user_id, inputs=[20.0, 5.0, 3.0, 2.0])
        assert calc.get_result() == 10.0
    
    def test_subtraction_negative_result(self):
        """Test subtraction resulting in negative number"""
        user_id = uuid.uuid4()
        calc = Subtraction(user_id=user_id, inputs=[5.0, 10.0])
        assert calc.get_result() == -5.0
    
    def test_subtraction_decimals(self):
        """Test subtracting decimal numbers"""
        user_id = uuid.uuid4()
        calc = Subtraction(user_id=user_id, inputs=[10.5, 3.2])
        assert calc.get_result() == pytest.approx(7.3)
    
    def test_subtraction_invalid_inputs(self):
        """Test subtraction with invalid inputs raises error"""
        user_id = uuid.uuid4()
        calc = Subtraction(user_id=user_id, inputs=[1.0])
        with pytest.raises(ValueError, match="at least two numbers"):
            calc.get_result()


class TestMultiplication:
    """Test Multiplication calculation logic"""
    
    def test_multiplication_two_numbers(self):
        """Test multiplying two numbers"""
        user_id = uuid.uuid4()
        calc = Multiplication(user_id=user_id, inputs=[4.0, 5.0])
        assert calc.get_result() == 20.0
    
    def test_multiplication_multiple_numbers(self):
        """Test multiplying multiple numbers"""
        user_id = uuid.uuid4()
        calc = Multiplication(user_id=user_id, inputs=[2.0, 3.0, 4.0])
        assert calc.get_result() == 24.0
    
    def test_multiplication_with_zero(self):
        """Test multiplication with zero"""
        user_id = uuid.uuid4()
        calc = Multiplication(user_id=user_id, inputs=[5.0, 0.0])
        assert calc.get_result() == 0.0
    
    def test_multiplication_negative_numbers(self):
        """Test multiplication with negative numbers"""
        user_id = uuid.uuid4()
        calc = Multiplication(user_id=user_id, inputs=[-2.0, 3.0])
        assert calc.get_result() == -6.0
    
    def test_multiplication_decimals(self):
        """Test multiplying decimal numbers"""
        user_id = uuid.uuid4()
        calc = Multiplication(user_id=user_id, inputs=[2.5, 4.0])
        assert calc.get_result() == 10.0
    
    def test_multiplication_invalid_inputs(self):
        """Test multiplication with invalid inputs raises error"""
        user_id = uuid.uuid4()
        calc = Multiplication(user_id=user_id, inputs=[1.0])
        with pytest.raises(ValueError, match="at least two numbers"):
            calc.get_result()


class TestDivision:
    """Test Division calculation logic"""
    
    def test_division_two_numbers(self):
        """Test dividing two numbers"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[12.0, 3.0])
        assert calc.get_result() == 4.0
    
    def test_division_multiple_numbers(self):
        """Test dividing multiple numbers sequentially"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[24.0, 2.0, 3.0])
        assert calc.get_result() == 4.0
    
    def test_division_decimals(self):
        """Test dividing decimal numbers"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[10.5, 2.0])
        assert calc.get_result() == pytest.approx(5.25)
    
    def test_division_by_zero_raises_error(self):
        """Test division by zero raises ValueError"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[10.0, 0.0])
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.get_result()
    
    def test_division_by_zero_in_sequence(self):
        """Test division by zero in sequence raises error"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[10.0, 2.0, 0.0])
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.get_result()
    
    def test_division_negative_numbers(self):
        """Test division with negative numbers"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[-12.0, 3.0])
        assert calc.get_result() == -4.0
    
    def test_division_invalid_inputs(self):
        """Test division with invalid inputs raises error"""
        user_id = uuid.uuid4()
        calc = Division(user_id=user_id, inputs=[1.0])
        with pytest.raises(ValueError, match="at least two numbers"):
            calc.get_result()


class TestCalculationModel:
    """Test general Calculation model behavior"""
    
    def test_calculation_repr(self):
        """Test string representation of calculation"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[1.0, 2.0])
        repr_str = repr(calc)
        assert 'addition' in repr_str
        assert '[1.0, 2.0]' in repr_str
    
    def test_calculation_has_user_id(self):
        """Test calculation stores user_id"""
        user_id = uuid.uuid4()
        calc = Addition(user_id=user_id, inputs=[1.0, 2.0])
        assert calc.user_id == user_id
    
    def test_calculation_type_is_set(self):
        """Test calculation type is set correctly"""
        user_id = uuid.uuid4()
        add_calc = Addition(user_id=user_id, inputs=[1.0, 2.0])
        sub_calc = Subtraction(user_id=user_id, inputs=[1.0, 2.0])
        mul_calc = Multiplication(user_id=user_id, inputs=[1.0, 2.0])
        div_calc = Division(user_id=user_id, inputs=[1.0, 2.0])
        
        assert add_calc.type == 'addition'
        assert sub_calc.type == 'subtraction'
        assert mul_calc.type == 'multiplication'
        assert div_calc.type == 'division'
