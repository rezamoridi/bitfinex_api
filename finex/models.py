from pydantic import BaseModel, Field, field_validator, ValidationError
from tools.symbols import symbols
from datetime import datetime

"""planting Models""" 

class Data(BaseModel):
    symbol : str = Field(min_length=6)
    start_date: str
    end_date: str
    time_frame: str

    @field_validator("symbol")
    @classmethod
    def symbol_validator(cls, v):
        if v not in symbols:
            raise ValueError("symbol not found")
        return v
    
    @field_validator("start_date", "end_date")
    @classmethod
    def valid_date(cls, v):
        date_obj = datetime.strptime(v, "%Y-%m-%d")
        
        if not isinstance(date_obj, datetime):
            raise ValueError("invalid date format")
        return v

    @field_validator("time_frame")
    @classmethod
    def valid_timeframe(cls, v):
        if v not in ["1m", "5m", "15m", "30m", "1h", "3h", "6h", "12h", "1D", "1W", "14D", "1M"]:
            raise ValueError("invalid time frame")
        return v
    
