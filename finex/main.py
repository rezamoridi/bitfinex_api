from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from bitfinex_api import get_bitfinex_price_data
from write_csv import save_to_csv as w_csv
from models import Data

templates = Jinja2Templates(directory="../templates")
app = FastAPI()
app.mount("/statics", StaticFiles(directory="../statics"), name="index")



@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)

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
    

    
@app.post('/download_csv')
def download(request: Request):
    w_csv(data_list, f"../csv/{data.symbol}-{data.start_date}-{data.end_date}-{data.time_frame}.csv")
    
    return templates.TemplateResponse(name="download.html", request=request)
    