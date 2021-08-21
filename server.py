from typing import List, Dict, Set

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from main import get_message, execute
from fastapi.staticfiles import StaticFiles

from model import Query, MessageMeta

app: FastAPI = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, channel_link: str = 'https://t.me/merosharekhabargroup',
                    search: str = '', filter: str = '', limit: int = 10, by_user: str = ''):
    query = Query(
        channel_link=channel_link,
        search=search,
        filter=filter,
        limit=limit,
        by_user=by_user,
    )
    result: List[MessageMeta] = await execute(query=query, block=get_message)
    return templates.TemplateResponse("messages.html", context={
        'request': request,
        "messages": result
    })


@app.get("/statistics", response_class=HTMLResponse)
async def read_root(
        request: Request, limit: int = 200,
        channel_link: str = 'https://t.me/merosharekhabargroup',
        search: str = ''):
    query = Query(
        channel_link=channel_link,
        search='',
        filter='',
        limit=limit,
        by_user='',
    )
    keywords = set(filter(lambda x: len(x) > 0, set(map(lambda x: x.strip().upper(), search.split(',')))))
    if len(keywords) == 0:
        return templates.TemplateResponse("statistics.html", context={
            'request': request,
            "counters": {}
        })
    result: List[MessageMeta] = await execute(query=query, block=get_message)
    counter: Dict[str, List[MessageMeta]] = {}
    repeated_msg_records: Set[str] = set()
    for msg in map(lambda x: x, result):
        if msg.full_message in repeated_msg_records:
            continue
        repeated_msg_records.add(msg.full_message)
        if msg.full_message is None:
            continue
        for word in msg.full_message.split(' '):
            upper = word.upper()
            if upper in keywords:
                stats = counter.get(upper)
                if stats is None:
                    stats = []
                stats.append(msg)
                counter[upper] = stats
    return templates.TemplateResponse("statistics.html", context={
        'request': request,
        "counters": counter
    })
