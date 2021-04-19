from time import strftime, localtime
from argparse import Namespace

from .data import *


def handle_link(args: Namespace) -> Namespace:
    send_type = "user" if args.send_user_id else "group"
    send_conv_id = args.send_user_id if send_type == "user" else args.send_group_id

    if args.origin in get_conv_mapping():
        args.message = "已链接其他会话！"
    else:
        user_id = args.user if hasattr(args, "user") else None
        group_id = args.group if hasattr(args, "group") else None
        link_conv(args.origin, user_id, group_id)
        args.message = "会话链接成功！"

    return args


def handle_unlink(args: Namespace) -> Namespace:
    args.user_id = args.origin

    if args.origin not in get_conv_mapping():
        args.message = "尚未链接任何会话！"
    else:
        unlink_conv(args.origin)
        args.message = "已解除链接！"

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


def handle_transmit(args: Namespace) -> Namespace:
    conv_mapping = get_conv_mapping()
    reverse_conv_mapping = get_conv_mapping(reverse=True)

    send_type = "user" if args.send_user_id else "group"
    send_conv_id = args.send_user_id if send_type == "user" else args.send_group_id
    args.recv_args = []

    for mapping in conv_mapping, reverse_conv_mapping:
        if send_conv_id in mapping[send_type]:
            for recv_type in mapping[send_type][send_conv_id]:
                for recv_conv_id in mapping[send_type][send_conv_id][recv_type]:
                    args.recv_args.append(
                        [
                            recv_conv_id if recv_type == "user" else None,
                            recv_conv_id if recv_type == "group" else None,
                            f"{args.name} {strftime('%Y-%m-%d %H:%M:%S',localtime(args.time))}\n  {args.message}"
                            if mapping == reverse_conv_mapping
                            else args.message,
                        ]
                    )

    return args
