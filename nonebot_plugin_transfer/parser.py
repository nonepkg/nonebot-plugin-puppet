from nonebot.rule import ArgumentParser

from .handle import *

transfer_parser = ArgumentParser("trans")

transfer_subparsers = transfer_parser.add_subparsers()

link_parser = transfer_subparsers.add_parser(
    "link", help="Link convsations with another what you want"
)
link_parser.add_argument("-ua", "--user-a",action="store", nargs="*", type=int)
link_parser.add_argument("-ga", "--group-a",action="store", nargs="*", type=int)
link_parser_group = link_parser.add_argument_group(required=True)
link_parser_group.add_argument("-u","-ub", "--user-b",action="store", nargs="+", type=int)
link_parser_group.add_argument("-g","-gb", "--group-b",action="store", nargs="+", type=int)
link_parser.set_defaults(handle=handle_link)

unlink_parser = transfer_subparsers.add_parser(
    "unlink", help="Unlink current conv_parser"
)
unlink_parser.add_argument("-ua", "--user-a",action="store", nargs="+", type=int)
unlink_parser.add_argument("-ga", "--group-a",action="store", nargs="+", type=int)
unlink_parser.add_argument("-u","-ub", "--user-b",action="store", nargs="+", type=int)
unlink_parser.add_argument("-g","-gb", "--group-b",action="store", nargs="+", type=int)
unlink_parser.set_defaults(handle=handle_unlink)

clear_parser = transfer_subparsers.add_parser(
    "clear", help="Unlink current conv_parser"
)
clear_parser.add_argument("-u", "--user",action="store", nargs="+", type=int)
clear_parser.add_argument("-g", "--group",action="store", nargs="+", type=int)
clear_parser.set_defaults(handle=handle_clear)

list_parser = transfer_subparsers.add_parser("list")
list_parser_group = list_parser.add_mutually_exclusive_group()
list_parser_group.add_argument("-u", "--user", action="store", type=int)
list_parser_group.add_argument("-g", "--group", action="store", type=int)
list_parser.set_defaults(handle=handle_list)

send_parser = transfer_subparsers.add_parser(
    "send", help="Send message to current conv_parser"
)
send_parser.add_argument("message", action="store")
send_parser.add_argument("-u", "--user", action="store", type=int)
send_parser.add_argument("-g", "--group", action="store", type=int)
send_parser.add_argument("-a", "--all", action="store_true")
send_parser.set_defaults(handle=handle_send)
