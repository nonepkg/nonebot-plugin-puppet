from nonebot.rule import ArgumentParser

from .handle import *

puppet_parser = ArgumentParser("puppet")

puppet_subparsers = puppet_parser.add_subparsers()

link_parser = puppet_subparsers.add_parser(
    "link", help="Link convsations with another what you want"
)
link_parser.add_argument(
    "-ua", "--user-a", action="store", nargs="*", default=[], type=int
)
link_parser.add_argument(
    "-ga", "--group-a", action="store", nargs="*", default=[], type=int
)
link_parser.add_argument(
    "-u", "-ub", "--user-b", action="store", nargs="+", default=[], type=int
)
link_parser.add_argument(
    "-g", "-gb", "--group-b", action="store", nargs="+", default=[], type=int
)
link_parser.add_argument("-q", "--quiet", action="store_true")
link_parser.set_defaults(handle=handle_link)

unlink_parser = puppet_subparsers.add_parser(
    "unlink", help="Unlink current conv_parser"
)
unlink_parser.add_argument(
    "-ua", "--user-a", action="store", nargs="+", default=[], type=int
)
unlink_parser.add_argument(
    "-ga", "--group-a", action="store", nargs="+", default=[], type=int
)
unlink_parser.add_argument(
    "-u", "-ub", "--user-b", action="store", nargs="+", default=[], type=int
)
unlink_parser.add_argument(
    "-g", "-gb", "--group-b", action="store", nargs="+", default=[], type=int
)
unlink_parser.add_argument("-q", "--quiet", action="store_true")
unlink_parser.set_defaults(handle=handle_unlink)

list_parser = puppet_subparsers.add_parser("list")
list_parser_group = list_parser.add_mutually_exclusive_group()
list_parser_group.add_argument("-u", "--user", action="store", type=int)
list_parser_group.add_argument("-g", "--group", action="store", type=int)
list_parser.set_defaults(handle=handle_list)

send_parser = puppet_subparsers.add_parser(
    "send", help="Send message to current conv_parser"
)
send_parser.add_argument("message", action="store")
send_parser.add_argument(
    "-u", "--user", action="store", nargs="+", default=[], type=int
)
send_parser.add_argument(
    "-g", "--group", action="store", nargs="+", default=[], type=int
)
send_parser.add_argument("-a", "--all", action="store_true")
send_parser.set_defaults(handle=handle_send)
