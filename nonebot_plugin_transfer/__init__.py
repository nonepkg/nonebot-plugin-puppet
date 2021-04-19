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

from .parser import Namespace, transfer_parser, handle_transmit

transfer_command = on_shell_command(
    "trans", parser=transfer_parser, priority=1, permission=SUPERUSER
)
transfer_transmit = on_message(priority=10, block=False)


@transfer_command.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    args.send_user_id, args.send_group_id = None, None
    if isinstance(event, PrivateMessageEvent):
        args.send_user_id = event.user_id
    elif isinstance(event, GroupMessageEvent):
        args.send_group_id = event.group_id
    if hasattr(args, "message"):
        args.message = unescape(args.message)

    if hasattr(args, "handle"):
        args = args.handle(args)
        if args.message:
            for recv_user_id, recv_group_id in args.recv_conv_id:
                await bot.send_msg(
                    user_id=recv_user_id,
                    group_id=recv_group_id,
                    message=Message(args.message),
                )


@transfer_transmit.handle()
async def _(bot: Bot, event: Event):

    args = Namespace()
    args.handle = handle_transmit
    args.send_user_id, args.send_group_id = None, None
    args.time = event.time
    args.message = unescape(str(event.get_message()))
    if isinstance(event, PrivateMessageEvent):
        args.send_user_id = event.user_id
        args.name = event.sender.nickname
    elif isinstance(event, GroupMessageEvent):
        args.send_group_id = event.group_id
        args.group_name = (await bot.get_group_info(event.group_id))["group_name"]
        args.name = event.sender.card if event.sender.card else event.sender.nickname

    if hasattr(args, "handle"):
        args = args.handle(args)
        if args.message:
            for recv_user_id, recv_group_id, message in args.recv_args:
                print(recv_user_id, recv_group_id, message)
                await bot.send_msg(
                    user_id=recv_user_id,
                    group_id=recv_group_id,
                    message=Message(message),
                )
