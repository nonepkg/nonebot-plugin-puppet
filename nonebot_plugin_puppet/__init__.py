from time import strftime, localtime
from argparse import Namespace
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_message, on_request, on_shell_command
from nonebot.params import ShellCommandArgs
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    RequestEvent,
    FriendRequestEvent,
    GroupRequestEvent,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    unescape,
)

from nonebot_plugin_puppet.parser import parser
from nonebot_plugin_puppet.handle import Handle
from nonebot_plugin_puppet.mapping import ConvMapping
from nonebot_plugin_puppet.request import ReqList

command = on_shell_command("puppet", parser=parser, priority=1, permission=SUPERUSER)
message = on_message(priority=10, block=False)
request = on_request(priority=10, block=False)


@command.handle()
async def _(bot: Bot, event: MessageEvent, args: Namespace = ShellCommandArgs()):
    ConvMapping().update_conv(
        {
            "user": [user["user_id"] for user in (await bot.get_friend_list())],
            "group": [group["group_id"] for group in (await bot.get_group_list())],
        },
    )

    args.conv_s = {
        "user": [event.user_id] if isinstance(event, PrivateMessageEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    args.conv_r = {"user": {}, "group": {}}

    if hasattr(args, "handle"):
        if hasattr(args, "message"):
            args.message = unescape(args.message)
        args = getattr(Handle, args.handle)(args)
        if hasattr(args, "req"):
            for type in args.req:
                for flag in args.req[type]:
                    try:
                        if type == "friend":
                            await bot.set_friend_add_request(
                                flag=flag, approve=args.req[type][flag]
                            )
                        elif type in ["add", "invite"]:
                            await bot.set_group_add_request(
                                flag=flag,
                                sub_type=type,
                                approve=args.req[type][flag],
                            )
                    except:
                        pass
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
        if args.handle == "exit":
            for id in args.group:
                try:
                    await bot.set_group_leave(group_id=id)
                except:
                    pass
    else:
        await bot.send(event, args.message)


@message.handle()
async def _(bot: Bot, event: MessageEvent):
    ConvMapping().update_conv(
        {
            "user": [user["user_id"] for user in (await bot.get_friend_list())],
            "group": [group["group_id"] for group in (await bot.get_group_list())],
        },
    )

    conv_s = {
        "user": [event.user_id] if isinstance(event, PrivateMessageEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    conv_r = ConvMapping().get_conv(conv_s)

    header = ""
    sender = ""
    message = unescape(str(event.get_message()))
    if str(event.user_id) not in bot.config.superusers:
        if isinstance(event, GroupMessageEvent):
            header = (await bot.get_group_info(group_id=event.group_id))[
                "group_name"
            ] + f" ({event.group_id})\n"
        sender = (
            event.sender.card
            if isinstance(event, GroupMessageEvent) and event.sender.card
            else event.sender.nickname
        ) + f" {strftime('%Y-%m-%d %H:%M:%S', localtime(event.time))} \n"
    message = header + sender + message

    for type in conv_r:
        for id in conv_r[type]:
            try:
                await bot.send_msg(
                    user_id=id if type == "user" else None,
                    group_id=id if type == "group" else None,
                    message=Message(message),
                )
            except:
                pass


@request.handle()
async def _(bot: Bot, event: RequestEvent):
    conv_s = {
        "user": [event.user_id] if isinstance(event, FriendRequestEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupRequestEvent) else [],
    }
    type = (
        event.sub_type if isinstance(event, GroupRequestEvent) else event.request_type
    )
    ReqList().add_req(
        {
            "friend": [event.flag] if type == "friend" else [],
            "invite": [event.flag] if type == "invite" else [],
            "add": [event.flag] if type == "add" else [],
        }
    )
    conv_r = (
        ConvMapping().get_conv(conv_s)
        if type == "add"
        else {"group": [], "user": [int(i) for i in bot.config.superusers]}
    )
    if type == "add":
        conv_r["group"].append(event.group_id)

    if str(event.user_id) not in bot.config.superusers:
        header = f"【请求】{event.flag}\n"
        sender = (await bot.get_stranger_info(user_id=event.user_id))[
            "nickname"
        ] + f" {strftime('%Y-%m-%d %H:%M:%S', localtime(event.time))} \n"
        message = (
            ("邀请" if type == "invite" else "请求")
            + (
                "添加为好友"
                if type == "friend"
                else "加入群聊"
                + (await bot.get_group_info(group_id=event.group_id))["group_name"]
                + f" ({event.group_id})\n"
            )
            + (f"\n备注：{event.comment}" if event.comment else "")
        )
        message = header + sender + message

        for type in conv_r:
            for id in conv_r[type]:
                try:
                    await bot.send_msg(
                        user_id=id if type == "user" else None,
                        group_id=id if type == "group" else None,
                        message=Message(message),
                    )
                except:
                    pass
    else:
        try:
            await event.approve(bot)
        except:
            pass
