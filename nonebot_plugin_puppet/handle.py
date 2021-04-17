from argparse import Namespace

from .data import *


def handle_link(args: Namespace) -> Namespace:
    args.user_id = args.origin

    if args.origin in get_conv_mapping():
        args.message = "已链接其他会话！"
    else:
        user_id = args.user if hasattr(args, "user") else None
        group_id = args.group if hasattr(args, "group") else None
        link_conv(args.origin, user_id, group_id)
        args.message = "会话链接成功！"

    return args


def handle_send(args: Namespace) -> Namespace:
    conv_mapping = get_conv_mapping()

    if args.origin not in conv_mapping:
        args.user_id = args.origin
        args.message = "尚未链接任何会话！"
    else:
        args.user_id = conv_mapping[args.origin]["user_id"]
        args.group_id = conv_mapping[args.origin]["group_id"]
    return args


def handle_unlink(args: Namespace) -> Namespace:
    args.user_id = args.origin

    if args.origin not in get_conv_mapping():
        args.message = "尚未链接任何会话！"
    else:
        unlink_conv(args.origin)
        args.message = "已解除链接！"

    return args
