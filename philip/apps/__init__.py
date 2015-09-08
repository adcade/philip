from philip.apps import create, update, get, restart, delete, list, version


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('apps', help='api for apps').add_subparsers()

    for sub_command in [create, update, get, restart, delete, list, version]:
        sub_command.register_command(sub_subparsers)
