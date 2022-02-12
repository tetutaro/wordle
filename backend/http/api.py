#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.model.wordle import Wordle

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
wordle = Wordle(logger=logging.getLogger('uvicorn'))


@app.get('/', status_code=status.HTTP_200_OK)
async def root(request: Request):
    info = wordle.get_info()
    return templates.TemplateResponse(
        'wordle.html',
        {'request': request, 'info': info}
    )


@app.get('/key/{key}', status_code=status.HTTP_200_OK)
async def append_letter(request: Request, key: str):
    wordle.append_letter(key=key)
    info = wordle.get_info()
    return templates.TemplateResponse(
        'wordle.html',
        {'request': request, 'info': info}
    )


@app.get('/return', status_code=status.HTTP_200_OK)
async def confirm_word(request: Request):
    wordle.confirm_word()
    info = wordle.get_info()
    return templates.TemplateResponse(
        'wordle.html',
        {'request': request, 'info': info}
    )


@app.get('/delete', status_code=status.HTTP_200_OK)
async def delete_letter(request: Request):
    wordle.delete_letter()
    info = wordle.get_info()
    return templates.TemplateResponse(
        'wordle.html',
        {'request': request, 'info': info}
    )


@app.get('/reset', status_code=status.HTTP_200_OK)
async def reset_game(request: Request):
    wordle.reset_game()
    info = wordle.get_info()
    return templates.TemplateResponse(
        'wordle.html',
        {'request': request, 'info': info}
    )
