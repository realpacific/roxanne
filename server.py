from typing import List

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from main import get_message, execute
from essential_generators import DocumentGenerator

from collections import Counter
from fastapi.staticfiles import StaticFiles

from model import Query

gen = DocumentGenerator()
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
    print(query)
    result: List[str] = await execute(query=query, block=get_message)
    # result = [gen.paragraph() for i in range(0, 10)]
    words = []
    for sentence in set(result):
        for word in sentence.split(' '):
            words.append(word)
    counter = Counter(words)
    print(counter.most_common(5))
    return templates.TemplateResponse("messages.html", context={
        'request': request,
        "messages": result
    })
