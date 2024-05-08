from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from tools import bitfinex_api as api
from tools import write_csv as csvtool

router = APIRouter()

@router.get("/candle/")
def canle(sy: str, sd: str, ed: str, tf: str, csv: bool):
    try:
        data = api.get_bitfinex_price_data_candle(symbol=sy, start_date=sd, end_date=ed, timeframe=tf)

        if csv:
            csvtool.save_to_csv(data=data, filename=f"../csv/candle_csv/{sy}-{sd}-{ed}-{tf}.csv")
            return "CSV saved!"
        else:
            return data
    
    except ValidationError as e:
        return HTTPException(status_code=400, detail=e.errors)