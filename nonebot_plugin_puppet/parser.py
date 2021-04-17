from nonebot.rule import ArgumentParser

from .handle import *

puppet_parser = ArgumentParser("puppet")

puppet_subparsers = puppet_parser.add_subparsers()

link_parser = puppet_subparsers.add_parser(
    "link", help="Link conversation what you want"
)
conversation = link_parser.add_mutually_exclusive_group()
conversation.add_argument("-u", "--user", action="store", type=int)
conversation.add_argument("-g", "--group", action="store", type=int)
link_parser.set_defaults(handle=handle_link)

send_parser = puppet_subparsers.add_parser(
    "send", help="Send message to current conversation"
)
send_parser.add_argument("message", action="store")
send_parser.set_defaults(handle=handle_send)

unlink_parser = puppet_subparsers.add_parser(
    "unlink", help="Unlink current conversation"
)
unlink_parser.set_defaults(handle=handle_unlink)
