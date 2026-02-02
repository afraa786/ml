from fastapi import FastAPI, Request, Response
import time

app =  FastAPI()

# call_next to call the next endpoint
@app.middleware("http")
async def log_request_time(request: Request, call_next):

