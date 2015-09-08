from philip.events import stream


def register_command(subparsers):
    sub_subparsers = subparsers.add_parser('events', help='api for events').add_subparsers()

    for sub_command in [stream]:
        sub_command.register_command(sub_subparsers)
