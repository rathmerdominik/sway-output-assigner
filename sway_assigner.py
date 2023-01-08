import argparse

from json import load
from subprocess import Popen, PIPE

from models.args import Args

parser = argparse.ArgumentParser(
    description="Output binding generator for SwayWM. Works for up to 2 monitor."
)
parser.add_argument(
    "-M",
    "--monitor",
    type=str,
    help="Set a monitor or multiple to work with. If not defined it will be interactive. The order you specify the monitors will be the order in the monitor array",
    action="extend",
    nargs="+",
)
parser.add_argument(
    "-o",
    "--get_outputs",
    action="store_true",
    help="Will print all available monitor names",
)
parser.add_argument(
    "-b", "--bind", action="store_true", help="Only prints monitor workspace bindings"
)
parser.add_argument(
    "-m", "--move", action="store_true", help="Only prints move bindings"
)
parser.add_argument(
    "-s", "--select", action="store_true", help="Prints only select binding"
)


def get_outputs() -> list[str]:
    cmd = Popen(("swaymsg", "--raw", "--type", "get_outputs"), stdout=PIPE)
    cmd.wait()
    raw_data: str = load(cmd.stdout)
    outputs: list[str] = []

    for output in raw_data:
        if output["type"] != "output":
            continue
        identifier: str = " ".join((output["make"], output["model"], output["serial"]))
        outputs.append(identifier)

    return outputs


def generate_workspace_select(outputs: list[str]) -> list[str]:
    selects = []
    for i in range(1, 11):
        if i < 10:
            selects.append(f"bindsym $mod+{i} workspace {i}")
        if i == 10:
            selects.append(f"bindsym $mod+0 workspace {i}")

    if len(outputs) > 1:
        for i in range(1, 11):
            selects.append(f"bindsym $mod+F{i} workspace {i + 10}")

    return selects


def generate_workspace_move(outputs: list[str]) -> list[str]:
    moves = []
    for i in range(1, 11):
        if i < 10:
            moves.append(f"bindsym $mod+Shift+{i} workspace {i}")
        if i == 10:
            moves.append(f"bindsym $mod+Shift+0 workspace {i}")

    if len(outputs) > 1:
        for i in range(1, 11):
            moves.append(f"bindsym $mod+Shift+F{i} workspace {i + 10}")

    return moves


def generate_workspace_bind(outputs: list[str]) -> list[str]:
    bindings = []
    for i in range(1, 21):
        if i < 11:
            bindings.append(f"workspace '{i}' output '{outputs[0]}'")
        else:
            bindings.append(f"workspace '{i}' output '{outputs[1]}'")
    return bindings


if __name__ == "__main__":
    args = Args(**vars(parser.parse_args()))
    outputs = get_outputs()

    if args.get_outputs:
        for output in outputs:
            print(output)
        exit(0)

    if not args.monitor:
        try:
            monitors = []
            print("+--+ Entering interactive mode +--+\n")
            for monitor in outputs:
                try:
                    pos = int(
                        input(
                            f"{monitor}\nWhich position does this monitor have? [int] > "
                        )
                    )
                except ValueError:
                    print(
                        "You did not insert a valid integer! Only integers can be used as monitor position"
                    )
                    exit(1)

                monitors.insert(pos + -1, monitor)

            args.monitor = monitors
        except KeyboardInterrupt:
            print("\nClosed on user request. Goodbye")
            exit(0)

    bindings = []
    if args.bind:
        bindings = generate_workspace_bind(args.monitor)

    selects = []
    if args.select:
        selects = generate_workspace_select(args.monitor)

    moves = []
    if args.move:
        moves = generate_workspace_move(args.monitor)

    for binding in bindings:
        print(binding)

    for select in selects:
        print(select)

    for moves in moves:
        print(moves)
