from argparse import Namespace as BaseNamespace
from typing import List

from nonebot.rule import ArgumentParser

from nonebot_plugin_puppet.mapping import Conv
from nonebot_plugin_puppet.request import Req


class Namespace(BaseNamespace):
    user: List[int] = []
    group: List[int] = []
    user_a: List[int] = []
    group_a: List[int] = []
    user_b: List[int] = []
    group_b: List[int] = []
    conv_s: Conv
    conv_r: Conv
    req: Req
    handle: str
    message: str
    quiet: bool
    all: bool
    unidirect: bool


parser = ArgumentParser("puppet")

subparsers = parser.add_subparsers(dest="handle")

link_parent = subparsers.add_parser(
    "link", help="Link conv_a to conv_b", add_help=False
)
link_parent.add_argument(
    "-u", "-ua", "--user-a", action="store", nargs="+", default=[], type=int
)
link_parent.add_argument(
    "-g", "-ga", "--group-a", action="store", nargs="+", default=[], type=int
)
link_parent.add_argument(
    "-ub", "--user-b", action="store", nargs="*", default=[], type=int
)
link_parent.add_argument(
    "-gb", "--group-b", action="store", nargs="*", default=[], type=int
)
link_parent.add_argument("-q", "--quiet", action="store_true")
link_parent.add_argument("-U", "--unidirect", action="store_true")
subparsers.add_parser("ln", parents=[link_parent])
subparsers.add_parser("link", parents=[link_parent])

unlink_parent = subparsers.add_parser(
    "unlink", help="Remove links from conv_a to conv_b", add_help=False
)
unlink_parent.add_argument(
    "-u", "-ua", "--user-a", action="store", nargs="*", default=[], type=int
)
unlink_parent.add_argument(
    "-g", "-ga", "--group-a", action="store", nargs="*", default=[], type=int
)
unlink_parent.add_argument(
    "-ub", "--user-b", action="store", nargs="*", default=[], type=int
)
unlink_parent.add_argument(
    "-gb", "--group-b", action="store", nargs="*", default=[], type=int
)
unlink_parent.add_argument("-q", "--quiet", action="store_true")
unlink_parent.add_argument("-U", "--unidirect", action="store_true")
subparsers.add_parser("rm", parents=[unlink_parent])
subparsers.add_parser("unlink", parents=[unlink_parent])

list_parent = subparsers.add_parser(
    "list", help="List convs linked with conv", add_help=False
)
list_parent_group = list_parent.add_mutually_exclusive_group()
list_parent_group.add_argument("-u", "--user", action="store", type=int)
list_parent_group.add_argument("-g", "--group", action="store", type=int)
subparsers.add_parser("ls", parents=[list_parent])
subparsers.add_parser("list", parents=[list_parent])

send = subparsers.add_parser("send", help="Send message to conv")
send.add_argument("message", action="store")
send.add_argument("-u", "--user", action="store", nargs="+", default=[], type=int)
send.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
send.add_argument("-a", "--all", action="store_true")

approve_parent = subparsers.add_parser(
    "approve", help="Approve request", add_help=False
)
approve_parent.add_argument(
    "-f", "--flag", action="store", nargs="+", default=[], type=str
)
approve_parent.add_argument("-a", "--all", action="store_true")
subparsers.add_parser("aprv", parents=[approve_parent])
subparsers.add_parser("approve", parents=[approve_parent])

reject_parent = subparsers.add_parser("reject", help="Reject request", add_help=False)
reject_parent.add_argument(
    "-f", "--flag", action="store", nargs="+", default=[], type=str
)
reject_parent.add_argument("-a", "--all", action="store_true")
subparsers.add_parser("rej", parents=[reject_parent])
subparsers.add_parser("reject", parents=[reject_parent])

exit = subparsers.add_parser("exit", help="Exit group")
exit.add_argument("-g", "--group", action="store", nargs="+", default=[], type=int)
