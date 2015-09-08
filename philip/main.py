import argcomplete

from constants import HelpOnErrorArgumentParser
import apps
import tasks
import groups
import deployments
import server
import events


def main():
    parser = HelpOnErrorArgumentParser()
    subparsers = parser.add_subparsers(parser_class=HelpOnErrorArgumentParser, help='sub-command help')

    for sub_command in [apps, tasks, groups, deployments, server, events]:
        sub_command.register_command(subparsers)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)
