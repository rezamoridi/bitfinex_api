"""Imports
"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import ValidationError
import time

from bitfinex_api import get_bitfinex_price_data, get_bitfinex_api_ticker
from tools.write_csv import save_to_csv as w_csv
from tools.write_csv import save_to_csv_beta
from tools.time_convert import convert_timesnap
from models import Data

"""Globals
"""
templates = Jinja2Templates(directory="../templates")
app = FastAPI()
app.mount("/statics", StaticFiles(directory="../statics"), name="index")


"""EndPoints
"""
# Root
@app.get('/')
def root(request : Request):
    return templates.TemplateResponse(name="home.html", request=request)

#Home
@app.get('/{view}')
def home(request: Request, view : str):
    if view == 'ticker':
        return templates.TemplateResponse(name="ticker_home.html", request=request)
    else:
        return templates.TemplateResponse(name="home.html", request=request)

#Home Form
@app.post('/')
def home_form(request: Request, symbol: str = Form(...), startdate = Form(...), enddate = Form(...) ,timeframe: str = Form(...)):
    try:   
        global data_list, data
        data = Data(symbol=symbol, start_date=startdate, end_date=enddate, time_frame=timeframe)
        data_list = get_bitfinex_price_data(symbol=f"t{data.symbol}", start_date=data.start_date, end_date=data.end_date, timeframe=data.time_frame)
        if data_list == None:
            data_list = [0]
        return templates.TemplateResponse(name="show_data.html", request=request, context={"data_list": data_list})

    except ValidationError as e:
        return templates.TemplateResponse(name="home.html", request=request, context={"error": e.errors()[0]["msg"]}) 
    

# Ticker Form
@app.post('/ticker')
def ticker_download(request: Request, symbol: str = Form(...), channel_time: int = Form(...)):
    try:
        ticks = get_bitfinex_api_ticker(symbol=f"t{symbol}", channel_time=channel_time)
        save_to_csv_beta(ticks, f"../csv/ticker_csv/{symbol} - {convert_timesnap(time.time())}")
        return templates.TemplateResponse(name="dl_success.html", request=request)
    except Exception:
        raise HTTPException(status_code=500, detail="Error")

    


# Candle csv download
@app.post('/download_csv')
def download(request: Request):
    w_csv(data_list, f"../csv/candle_csv/{data.symbol}-{data.start_date}-{data.end_date}-{data.time_frame}.csv")
    
    return templates.TemplateResponse(name="dl_success.html", request=request)
    