import sys
import argparse

import Model
import View
import Controller

mdl = Model.Model()
cnt = Controller.Controller(mdl)


def parse_args():
    if len(sys.argv) < 2:
        return None
    parser = argparse.ArgumentParser(description="")
    _ = parser.add_argument(
        "-u", nargs=1, metavar="user_uuid", type=str, help="user uuid", default=[None]
    )
    _ = parser.add_argument(
        "-d",
        nargs=1,
        metavar="doc_uuid",
        type=str,
        help="document uuid",
        default=[None],
    )
    _ = parser.add_argument(
        "-t", nargs=1, metavar="task_id", type=str, help="task id", default=[None]
    )
    _ = parser.add_argument(
        "-f",
        nargs=1,
        metavar="file",
        type=argparse.FileType("r"),
        help="json file",
        default=[None],
    )
    _ = parser.add_argument(
        "--disable-cache",
        metavar="disable_cache",
        action="store_const",
        const=True,
        default=False,
        help="disable cache for file (create another file with the same name .pkl by default)",
    )
    _ = parser.add_argument(
        "--gui",
        metavar="graphics",
        action="store_const",
        const=True,
        default=False,
        help="use matplotlib render or basic text render",
    )
    args = parser.parse_args()
    return args


def gui_app():
    win = View.Window(cnt)
    win.mainloop()
    return 0


def main() -> int:
    args = parse_args()
    if args is None:
        return gui_app()
    task_id = args.t[0]
    doc_uuid = args.d[0]
    user_uuid = args.u[0]
    file = args.f[0]
    gui = True if args.gui else False
    disable_cache = True if args.disable_cache else False

    actions = {
        "2a": {
            True: cnt.view_by_country_graph,
            False: cnt.view_by_country_text,
            "args": [doc_uuid],
        },
        "2b": {
            True: cnt.view_by_continent_graph,
            False: cnt.view_by_continent_text,
            "args": [doc_uuid],
        },
        "3a": {
            True: cnt.view_by_full_browser_graph,
            False: cnt.view_by_full_browser_text,
            "args": ["all"],  # TODO: event type
        },
        "3b": {
            True: cnt.view_by_browser_graph,
            False: cnt.view_by_browser_text,
            "args": ["all"],  # TODO: event type
        },
        "4": {
            True: cnt.reader_profile_graph,
            False: cnt.reader_profile_text,
            "args": [],
        },
        "5d": {
            True: cnt.also_like_text,
            False: cnt.also_like_text,
            "args": [doc_uuid, user_uuid],
        },
        "6": {
            True: cnt.also_like_graph,
            False: cnt.also_like_graph,
            "args": [doc_uuid, user_uuid],
        },
        "7": {
            True: gui_app,
            False: gui_app,
            "args": [],
        },
    }
    if task_id not in actions.keys():
        print("task_id is unknown", file=sys.stderr)
        return 1

    action_task = actions[task_id]  # pyright: ignore[reportUnknownVariableType]
    action_task_fn = action_task[gui]
    if action_task_fn is None:
        print("task_id is unknown", file=sys.stderr)
        return 1
    if None in action_task["args"] or file is None:
        print("Arguments are missings", file=sys.stderr)
        return 1
    cnt.load_file(file.name, disable_cache)

    try:
        s = action_task_fn(
            *action_task["args"]  # pyright: ignore[reportCallIssue, reportArgumentType]
        )
    except ValueError as error:
        print(f"F21SCCW2: error: {error}", file=sys.stderr)
    else:
        if s is not None:
            s = f"{s}"
            print(s)
    return 0


if __name__ == "__main__":
    ret_code = main()
    sys.exit(ret_code)
