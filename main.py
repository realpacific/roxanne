from datetime import datetime, timedelta
from typing import Union, List, Callable, Any

from telethon import TelegramClient
from telethon.tl import types
from telethon.tl.types import PeerChat, InputMessagesFilterEmpty
from config import api_hash, api_id

from model import Query


async def get_message(query: Query, client: TelegramClient):
    now = datetime.now().astimezone()
    channel: types.Channel = await client.get_entity(query.channel_link)
    chat: types.Chat = await client.get_entity(channel.id)
    users: List[types.TypeChatParticipant] = []

    if query.by_user is not None and len(query.by_user.strip()) > 0:
        async for part in client.iter_participants(chat, search=query.by_user.strip()):
            print(part.first_name, part.last_name, part.id)
            users.append(part)

    result = []
    async for message in client.iter_messages(
            chat, limit=query.limit,
            filter=Union[InputMessagesFilterEmpty],
            from_user=users[0].id if len(users) > 0 else None):
        message_date: datetime = message.date
        days = (now - message_date).days
        time = message_date.time()
        result.append(message.message)
    return result


async def execute(block: Callable[[Query, TelegramClient], Any], query: Query):
    async with TelegramClient('anon', api_id, api_hash) as client:
        result = await block(query, client)
        print(result)
        return result
