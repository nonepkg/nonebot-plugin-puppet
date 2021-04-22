from time import strftime, localtime
from argparse import Namespace as ArgNamespace

from .data import *


class Namespace(ArgNamespace):
    user_a: List[int] = []
    group_a: List[int] = []
    user_b: List[int] = []
    group_b: List[int] = []
    user: List[int] = []
    group: List[int] = []
    message: str
    conv_s: Conv
    conv_r: Conv


def handle_link(args: Namespace) -> Namespace:

    conv_a = (
        {"user": args.user_a, "group": args.group_a}
        if args.user_a or args.group_a
        else args.conv_s
    )
    conv_b = {"user": args.user_b, "group": args.group_b}

    result = ConvMapping().link_conv(conv_a, conv_b)

    if not args.quiet:
        for type_a in result:
            for id_a in result[type_a]:
                args.conv_r[type_a][
                    id_a
                ] = f"{'用户' if type_a == 'user' else '群'} {id_a} 已与以下会话建立链接:"
                for type_b in result[type_a][id_a]:
                    if result[type_a][id_a][type_b]:
                        args.conv_r[type_a][id_a] += (
                            "\n用户:" if type_b == "user" else "\n群:"
                        )
                        for id_b in result[type_a][id_a][type_b]:
                            if result[type_a][id_a][type_b][id_b]:
                                args.conv_r[type_a][id_a] += "\n" + str(id_b)

    return args


def handle_unlink(args: Namespace) -> Namespace:

    conv_a = (
        {"user": args.user_a, "group": args.group_a}
        if args.user_a or args.group_a
        else args.conv_s
    )
    conv_b = (
        {"user": args.user_b, "group": args.group_b}
        if args.user_a or args.group_b
        else ConvMapping().get_conv(args.conv_s)
    )

    result = ConvMapping().unlink_conv(conv_a, conv_b)

    if not args.quiet:
        for type_a in result:
            for id_a in result[type_a]:
                args.conv_r[type_a][
                    id_a
                ] = f"{'用户' if type_a == 'user' else '群'} {id_a} 已与以下会话解除链接:"
                for type_b in result[type_a][id_a]:
                    if result[type_a][id_a][type_b]:
                        args.conv_r[type_a][id_a] += (
                            "\n用户:" if type_b == "user" else "\n群:"
                        )
                        for id_b in result[type_a][id_a][type_b]:
                            if result[type_a][id_a][type_b][id_b]:
                                args.conv_r[type_a][id_a] += "\n" + str(id_b)

    return args


def handle_list(args: Namespace):

    conv = (
        ConvMapping().get_conv({"user": args.user, "group": args.group})
        if args.user or args.group
        else ConvMapping().get_conv(args.conv_s)
    )

    for type_s in args.conv_s:
        for id_s in args.conv_s[type_s]:
            args.conv_r[type_s][
                id_s
            ] = f"{'用户' if type_s == 'user' else '群'} {id_s} 的会话链接列表为:"
            for type in conv:
                if conv[type]:
                    args.conv_r[type_s][id_s] += "\n用户:" if type == "user" else "\n群:"
                    for id in conv[type]:
                        args.conv_r[type_s][id_s] += "\n" + str(id)

    return args


def handle_send(args: Namespace) -> Namespace:

    conv = (
        {"user": args.user, "group": args.group}
        if args.user or args.group
        else ConvMapping().get_conv(args.conv_s)
    )

    if args.all:
        conv = ConvMapping().get_conv()
        conv["user"] = []

    for type in conv:
        for id in conv[type]:
            args.conv_r[type][id] = args.message

    return args


def handle_transmit(args: Namespace) -> Namespace:

    conv = ConvMapping().get_conv(args.conv_s)

    if args.is_superuser:
        args.group = ""
        args.sender = ""
    else:
        args.sender = (
            f"{args.name} {strftime('%Y-%m-%d %H:%M:%S',localtime(args.time))} \n"
        )

    for type in conv:
        for id in conv[type]:
            args.conv_r[type][id] = args.group + args.sender + args.message
    return args
