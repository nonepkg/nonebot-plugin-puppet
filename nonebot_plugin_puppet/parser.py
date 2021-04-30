from nonebot.rule import ArgumentParser

puppet_parser = ArgumentParser("puppet")

puppet_subparsers = puppet_parser.add_subparsers(dest="handle")

link_parent = puppet_subparsers.add_parser(
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
link_parent.add_argument("-U", "--unilateral", action="store_true")
ln_parser = puppet_subparsers.add_parser("ln", parents=[link_parent])
link_parser = puppet_subparsers.add_parser("link", parents=[link_parent])

unlink_parent = puppet_subparsers.add_parser(
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
rm_parser = puppet_subparsers.add_parser("rm", parents=[unlink_parent])
unlink_parser = puppet_subparsers.add_parser("unlink", parents=[unlink_parent])

list_parent = puppet_subparsers.add_parser(
    "list", help="List convs linked with conv", add_help=False
)
list_parent_group = list_parent.add_mutually_exclusive_group()
list_parent_group.add_argument("-u", "--user", action="store", type=int)
list_parent_group.add_argument("-g", "--group", action="store", type=int)
ls_parser = puppet_subparsers.add_parser("ls", parents=[list_parent])
list_parser = puppet_subparsers.add_parser("list", parents=[list_parent])

send_parser = puppet_subparsers.add_parser("send", help="Send message to conv")
send_parser.add_argument("message", action="store")
send_parser.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
send_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
send_parser.add_argument("-a", "--all", action="store_true")
