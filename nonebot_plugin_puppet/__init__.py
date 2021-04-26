from nonebot_plugin_puppet.data import ConvMapping
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_message, on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    Message,
    MessageEvent,
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
async def _(bot: Bot, event: MessageEvent, state: T_State):
    ConvMapping().update_conv(
        {
            "user": [user["user_id"] for user in (await bot.get_friend_list())],
            "group": [group["group_id"] for group in (await bot.get_group_list())],
        },
    )

    args: Namespace = state["args"]

    args.conv_s = {
        "user": [event.user_id] if isinstance(event, PrivateMessageEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    args.conv_r = {"user": {}, "group": {}}

    if hasattr(args, "message"):
        args.message = unescape(args.message)

    if hasattr(args, "handle"):
        args = args.handle(args)
        for type in args.conv_r:
            for id in args.conv_r[type]:
                try:
                    await bot.send_msg(
                        user_id=id if type == "user" else None,
                        group_id=id if type == "group" else None,
                        message=Message(args.conv_r[type][id]),
                    )
                except:
                    pass


@puppet_transmit.handle()
async def _(bot: Bot, event: MessageEvent):
    ConvMapping().update_conv(
        {
            "user": [user["user_id"] for user in (await bot.get_friend_list())],
            "group": [group["group_id"] for group in (await bot.get_group_list())],
        },
    )

    args = Namespace()
    args.handle = handle_transmit

    args.conv_s = {
        "user": [event.user_id] if isinstance(event, PrivateMessageEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    args.conv_r = {"user": {}, "group": {}}

    args.group = (
        ""
        if isinstance(event, PrivateMessageEvent)
        else f"{(await bot.get_group_info(group_id=event.group_id))['group_name']}({event.group_id})\n"
    )
    args.name = (
        event.sender.card
        if isinstance(event, GroupMessageEvent) and event.sender.card
        else event.sender.nickname
    )
    args.time = event.time
    args.is_superuser = str(event.user_id) in bot.config.superusers
    args.message = unescape(str(event.get_message()))

    if hasattr(args, "handle"):
        args = args.handle(args)
        for type in args.conv_r:
            for id in args.conv_r[type]:
                try:
                    await bot.send_msg(
                        user_id=id if type == "user" else None,
                        group_id=id if type == "group" else None,
                        message=Message(args.conv_r[type][id]),
                    )
                except:
                    pass
