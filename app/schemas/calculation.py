"""
Pydantic schemas for Calculation validation.
Author: Pruthul Patel
Date: October 18, 2025
"""
import uuid
from typing import List, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CalculationCreate(BaseModel):
    """
    Schema for creating a new calculation.
    Validates input data before saving to database.
    """
    type: Literal['addition', 'subtraction', 'multiplication', 'division'] = Field(
        ...,
        description="Type of calculation to perform"
    )
    inputs: List[float] = Field(
        ...,
        min_length=2,
        description="List of numbers to calculate (minimum 2 numbers required)"
    )
    
    @field_validator('inputs')
    @classmethod
    def validate_inputs(cls, v, info):
        """Validate inputs based on calculation type"""
        if len(v) < 2:
            raise ValueError("At least two numbers are required")
        
        # Check for division by zero
        if info.data.get('type') == 'division':
            if any(num == 0 for num in v[1:]):
                raise ValueError("Cannot divide by zero")
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "addition",
                "inputs": [10.5, 20.3, 5.2]
            }
        }


class CalculationRead(BaseModel):
    """
    Schema for reading calculation data.
    Returns calculation with computed result.
    """
    id: uuid.UUID = Field(..., description="Unique calculation identifier")
    user_id: uuid.UUID = Field(..., description="ID of user who created the calculation")
    type: str = Field(..., description="Type of calculation")
    inputs: List[float] = Field(..., description="Input numbers used in calculation")
    result: float | None = Field(None, description="Calculated result")
    created_at: datetime = Field(..., description="When calculation was created")
    updated_at: datetime = Field(..., description="When calculation was last updated")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "type": "addition",
                "inputs": [10.5, 20.3, 5.2],
                "result": 36.0,
                "created_at": "2025-10-18T22:00:00",
                "updated_at": "2025-10-18T22:00:00"
            }
        }


class CalculationUpdate(BaseModel):
    """
    Schema for updating a calculation.
    Allows updating inputs and recalculating result.
    """
    inputs: List[float] = Field(
        ...,
        min_length=2,
        description="Updated list of numbers"
    )
    
    @field_validator('inputs')
    @classmethod
    def validate_inputs(cls, v):
        """Validate that we have at least 2 numbers"""
        if len(v) < 2:
            raise ValueError("At least two numbers are required")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "inputs": [15.5, 25.3, 10.2]
            }
        }