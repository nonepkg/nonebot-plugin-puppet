from nonebot.rule import ArgumentParser

from .handle import *

transfer_parser = ArgumentParser("trans")

transfer_subparsers = transfer_parser.add_subparsers()

link_parser = transfer_subparsers.add_parser(
    "link", help="Link conv_group what you want"
)
link_group = link_parser.add_mutually_exclusive_group()
link_group.add_argument("-u", "--user", action="store", type=int)
link_group.add_argument("-g", "--group", action="store", type=int)
link_parser.set_defaults(handle=handle_link)


unlink_parser = transfer_subparsers.add_parser(
    "unlink", help="Unlink current conv_group"
)
unlink_group = unlink_parser.add_mutually_exclusive_group()
unlink_group.add_argument("-u", "--user", action="store", type=int)
unlink_group.add_argument("-g", "--group", action="store", type=int)
unlink_parser.set_defaults(handle=handle_unlink)

send_parser = transfer_subparsers.add_parser(
    "send", help="Send message to current conv_group"
)
send_group = send_parser.add_mutually_exclusive_group()
send_group.add_argument("-u", "--user", action="store", type=int)
send_group.add_argument("-g", "--group", action="store", type=int)
send_parser.add_argument("message", action="store")
send_parser.set_defaults(handle=handle_send)
