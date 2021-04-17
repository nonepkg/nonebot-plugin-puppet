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
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    args = state["args"]
    args.origin = event.user_id
    args.user_id, args.group_id = None, None
    if hasattr(args, "message"):
        args.message = unescape(args.message)

    if hasattr(args, "handle"):
        args = args.handle(args)
        if args.message:
            await bot.send_msg(
                user_id=args.user_id,
                group_id=args.group_id,
                message=Message(args.message),
            )


@puppet_transmit.handle()
async def _(bot: Bot, event: Event):

    args = Namespace()
    args.handle = handle_transmit
    args.user_id, args.group_id = None, None
    args.time = event.time
    args.message = unescape(str(event.get_message()))
    if isinstance(event, PrivateMessageEvent):
        args.origin = event.user_id
        args.name = event.sender.nickname
    elif isinstance(event, GroupMessageEvent):
        args.origin = event.group_id
        args.name = event.sender.card if event.sender.card else event.sender.nickname

    if hasattr(args, "handle"):
        args = args.handle(args)
        if args.message:
            await bot.send_msg(
                user_id=args.user_id,
                group_id=args.group_id,
                message=Message(args.message),
            )
