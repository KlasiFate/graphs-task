from argparse import ArgumentParser

from .building_tree import add_subparser as building_tree_add_subparser

description = """
This program allow you to use some algorithms on graphs (all available algorithms see below).
"""


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="graphs-alg", description=description)
    subparsers = parser.add_subparsers(
        title="Available algorithms",
        help="Available algorithms is listed below",
        required=True,
        metavar="{algorithm-to-run}",
    )
    building_tree_add_subparser(subparsers)

    return parser


def run() -> None:
    parser = get_parser()
    options = parser.parse_args()
    options.cmd(options)
