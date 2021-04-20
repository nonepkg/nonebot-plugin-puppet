from nonebot.permission import SUPERUSER
from nonebot.plugin import on_message, on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    Message,
    Event,
    GroupMessageEvent,
    PrivateMessageEvent,
    unescape,
)

from .parser import Namespace, puppet_parser, handle_transmit

puppet_command = on_shell_command(
    "puppet", parser=puppet_parser, priority=1, permission=SUPERUSER
)
puppet_transmit = on_message(priority=10, block=False)


@puppet_command.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args: Namespace = state["args"]
    args.user_id, args.group_id = None, None
    if isinstance(event, PrivateMessageEvent):
        args.user_id = event.user_id
    elif isinstance(event, GroupMessageEvent):
        args.group_id = event.group_id
    if hasattr(args, "message"):
        args.message = unescape(args.message)
    args.recv_args = []
    if hasattr(args, "handle"):
        args = args.handle(args)
        for user_id, group_id, message in args.recv_args:
            await bot.send_msg(
                user_id=user_id,
                group_id=group_id,
                message=Message(message),
            )


@puppet_transmit.handle()
async def _(bot: Bot, event: Event):

    args = Namespace()
    args.handle = handle_transmit
    args.user_id, args.group_id = None, None
    args.time = event.time
    args.message = unescape(str(event.get_message()))
    args.is_superuser = str(event.user_id) in bot.config.superusers
    if isinstance(event, PrivateMessageEvent):
        args.user_id = event.user_id
        args.name = event.sender.nickname
        args.conv = ""
    elif isinstance(event, GroupMessageEvent):
        args.group_id = event.group_id
        args.name = event.sender.card if event.sender.card else event.sender.nickname
        args.conv = f"{(await bot.get_group_info(group_id=event.group_id))['group_name']}({event.group_id})\n"

    if hasattr(args, "handle"):
        args = args.handle(args)
        for user_id, group_id, message in args.recv_args:
            await bot.send_msg(
                user_id=user_id,
                group_id=group_id,
                message=Message(message),
            )
