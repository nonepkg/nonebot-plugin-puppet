from nonebot.permission import SUPERUSER
from nonebot.plugin import on_message, on_shell_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent, PrivateMessageEvent

from .data import get_conv_mapping
from .parser import puppet_parser

puppet = on_shell_command(
    "puppet", parser=puppet_parser, priority=1, permission=SUPERUSER
)
puppet_ = on_message(priority=10, block=False)


@puppet.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    args = state["args"]
    args.origin = event.user_id
    args.user_id, args.group_id = None, None
    if hasattr(args, "handle"):
        args = args.handle(args)
        if args.message:
            await bot.send_msg(
                user_id=args.user_id, group_id=args.group_id, message=args.message
            )


@puppet_.handle()
async def _(bot: Bot, event: Event):
    conv_mapping = get_conv_mapping()
    reverse_conv_mapping = get_conv_mapping(reverse=True)

    if isinstance(event, PrivateMessageEvent):
        origin = event.user_id
    elif isinstance(event, GroupMessageEvent):
        origin = event.group_id

    user_id, group_id = None, None

    if origin in reverse_conv_mapping:
        user_id = reverse_conv_mapping[origin]
    elif origin in conv_mapping:
        user_id = conv_mapping[origin]["user_id"]
        group_id = conv_mapping[origin]["group_id"]

    await bot.send_msg(user_id=user_id, group_id=group_id, message=event.get_message())
