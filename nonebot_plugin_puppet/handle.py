from typing import List, Set
from argparse import Namespace as ArgNamespace

from nonebot_plugin_puppet.mapping import Conv, ConvMapping
# from nonebot_plugin_puppet.request import ReqList


class Namespace(ArgNamespace):
    user: List[int] = []
    group: List[int] = []
    user_a: List[int] = []
    group_a: List[int] = []
    user_b: List[int] = []
    group_b: List[int] = []
    conv_s: Conv
    conv_r: Conv
    handle: str
    message: str


class Handle:
    @classmethod
    def ln(cls, args: Namespace) -> Namespace:
        return cls.link(args)

    @classmethod
    def link(cls, args: Namespace) -> Namespace:

        conv_a = {"user": args.user_a, "group": args.group_a}
        conv_b = (
            {"user": args.user_b, "group": args.group_b}
            if args.user_b or args.group_b
            else args.conv_s
        )

        result = ConvMapping().link_conv(conv_a, conv_b, args.unidirect)

        if not args.quiet:
            for type_b in result:
                for id_b in result[type_b]:
                    if result[type_b][id_b]["user"] or result[type_b][id_b]["group"]:
                        args.conv_r[type_b][
                            id_b
                        ] = f"{'用户' if type_b == 'user' else '群'} {id_b} 已与以下会话建立链接:"
                        for type_a in result[type_b][id_b]:
                            if result[type_b][id_b][type_a]:
                                args.conv_r[type_b][id_b] += (
                                    "\n用户:" if type_a == "user" else "\n群:"
                                )
                                for id_a in result[type_b][id_b][type_a]:
                                    args.conv_r[type_b][id_b] += "\n" + str(id_a)

        return args

    @classmethod
    def rm(cls, args: Namespace) -> Namespace:
        return cls.unlink(args)

    @classmethod
    def unlink(cls, args: Namespace) -> Namespace:

        conv_a = (
            {"user": args.user_a, "group": args.group_a}
            if args.user_a or args.group_a
            else ConvMapping().get_conv(args.conv_s, True)
        )
        conv_b = (
            {"user": args.user_b, "group": args.group_b}
            if args.user_b or args.group_b
            else args.conv_s
        )

        result = ConvMapping().unlink_conv(conv_a, conv_b, args.unidirect)

        if not args.quiet:
            for type_b in result:
                for id_b in result[type_b]:
                    if result[type_b][id_b]["user"] or result[type_b][id_b]["group"]:
                        args.conv_r[type_b][
                            id_b
                        ] = f"{'用户' if type_b == 'user' else '群'} {id_b} 已与以下会话解除链接:"
                        for type_a in result[type_b][id_b]:
                            if result[type_b][id_b][type_a]:
                                args.conv_r[type_b][id_b] += (
                                    "\n用户:" if type_a == "user" else "\n群:"
                                )
                                for id_a in result[type_b][id_b][type_a]:
                                    args.conv_r[type_b][id_b] += "\n" + str(id_a)

        return args

    @classmethod
    def ls(cls, args: Namespace):
        return cls.list(args)

    @classmethod
    def list(cls, args: Namespace):
        conv_a = (
            ConvMapping().get_conv({"user": args.user, "group": args.group})
            if args.user or args.group
            else ConvMapping().get_conv(args.conv_s, True)
        )
        conv_b = (
            ConvMapping().get_conv({"user": args.user, "group": args.group})
            if args.user or args.group
            else ConvMapping().get_conv(args.conv_s)
        )

        for type_s in args.conv_s:
            for id_s in args.conv_s[type_s]:
                args.conv_r[type_s][id_s] = ""
                for type in conv_a:
                    if conv_a[type] or conv_b[type]:
                        args.conv_r[type_s][id_s] += (
                            "\n用户:" if type == "user" else "\n群:"
                        )
                        for id in conv_a[type] + conv_b[type]:
                            if id not in args.conv_r[type_s][id_s]:
                                args.conv_r[type_s][
                                    id_s
                                ] += f"\n{'<' if id in conv_a[type] else '-'}--{'>' if id in conv_b[type] else '-'} {id}"
                if args.conv_r[type_s][id_s]:
                    args.conv_r[type_s][id_s] = (
                        f"{'用户' if type_s == 'user' else '群'} {id_s} 的会话列表为:"
                        + args.conv_r[type_s][id_s]
                    )

        return args

    @classmethod
    def send(cls, args: Namespace) -> Namespace:
        if not args.all:
            conv = (
                {"user": args.user, "group": args.group}
                if args.user or args.group
                else ConvMapping().get_conv(args.conv_s)
            )
        else:
            conv = ConvMapping().get_conv()
            conv["user"] = {}

        for type in conv:
            for id in conv[type]:
                args.conv_r[type][id] = args.message

        return args

    @classmethod
    def aprv(cls, args: Namespace) -> Namespace:
        return cls.approve(args)

    @classmethod
    def approve(cls, args: Namespace) -> Namespace:
        pass
