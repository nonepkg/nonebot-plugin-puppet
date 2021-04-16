from argparse import Namespace

from .data import *


def handle_link(
    args: Namespace,
    origin: int,
) -> str:
    if origin in get_conv_mapping():
        return "已链接其他会话！"

    user_id = args.user if hasattr(args, "user") else None

    group_id = args.group if hasattr(args, "group") else None

    link_conv(origin, user_id, group_id)

    return "会话链接成功！"


def handle_unlink(
    args: Namespace,
    origin: int,
) -> str:

    if origin not in get_conv_mapping():
        return "尚未链接任何会话！"

    unlink_conv(origin)

    return "已解除链接！"
