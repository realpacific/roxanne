from datetime import datetime
from typing import List, Callable, Any

from telethon import TelegramClient
from telethon.tl import types
from telethon.tl.types import PeerUser, InputMessagesFilterEmpty, Message

import config
from config import api_hash, api_id
from model import Query, MessageMeta

gen = None
if config.is_mock:
    from essential_generators import DocumentGenerator

    gen = DocumentGenerator()


async def get_message(query: Query, client: TelegramClient):
    channel: types.Channel = await client.get_entity(query.channel_link)
    chat: types.Chat = await client.get_entity(channel.id)
    users: List[types.TypeChatParticipant] = []

    if query.by_user is not None and len(query.by_user.strip()) > 0:
        async for part in client.iter_participants(chat, search=query.by_user.strip()):
            print(part.first_name, part.last_name, part.id)
            users.append(part)

    msg: Message
    result: List[MessageMeta] = []
    async for msg in client.iter_messages(
            chat, limit=query.limit,
            search=query.search,
            filter=InputMessagesFilterEmpty,
            from_user=users[0].id if len(users) > 0 else None):
        print(msg)
        meta = MessageMeta(
            author_id=msg.from_id.user_id if isinstance(msg.from_id, PeerUser) else None,
            full_message=msg.message, time=msg.date
        )
        result.append(meta)
    return result


async def execute(block: Callable[[Query, TelegramClient], Any], query: Query):
    if gen is not None:
        return map(
            lambda x: MessageMeta(author_id=x, full_message=gen.sentence(), time=datetime.now()),
            range(0, 10)
        )
    async with TelegramClient('anon', api_id, api_hash) as client:
        result = await block(query, client)
        return result
