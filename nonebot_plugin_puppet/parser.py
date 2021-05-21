from nonebot.rule import ArgumentParser

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

aprove_parent = subparsers.add_parser("approve", help="Aprove request", add_help=False)
aprove_parent.add_argument("message", action="store")
aprove_parent.add_argument(
    "-f", "--flag", action="store", nargs="+", default=[], type=str
)
aprove_parent.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
aprove_parent.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
aprove_parent.add_argument("-a", "--all", action="store_true")
subparsers.add_parser("aprv", parents=[aprove_parent])
subparsers.add_parser("approve", parents=[aprove_parent])
