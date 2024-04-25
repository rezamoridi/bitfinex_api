from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from bitfinex_api import get_bitfinex_price_data

templates = Jinja2Templates(directory="../templates")
app = FastAPI()
app.mount("/statics", StaticFiles(directory="../statics"), name="index")

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)

@app.post('/')
def home_form(request: Request, symbol: str = Form(...), startdate = Form(...), enddate = Form(...) ,timeframe: str = Form(...)):
    data = {"symbol": symbol,
            "startdate": startdate,
            "enddate": enddate,
            "timeframe": timeframe
            }
    
    data_csv = get_bitfinex_price_data(symbol=data["symbol"], start_date=data["startdate"], end_date=data["enddate"], timeframe=data["timeframe"])
    
    return templates.TemplateResponse(name="download.html", request=request, context={"data_csv": data_csv, "data": data})