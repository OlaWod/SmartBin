#!/usr/bin/env python3
from bottle import get,post,run,request,template
@get("/")
def index():
    return template("index")
@post("/cmd")
def cmd():
    print("按下按钮: "+request.body.read().decode())
run(host="0.0.0.0",port="8080")