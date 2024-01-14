import argparse

from run import run
from analyse import analyse, FUNCTION_MAPPING


def positive_int(arg: str):
    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if i <= 0:
        raise argparse.ArgumentTypeError("Argument must be greater than 0")
    return i


def vertex_number(arg: str):
    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if i < 4:
        raise argparse.ArgumentTypeError("Argument must be greater or equal 4")
    return i


def non_negative_int(arg: str):
    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be an integer number")
    if i < 0:
        raise argparse.ArgumentTypeError("Argument must be greater or equal 0")
    return i


class ModeMapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def run(args) -> None:
        run(args)

    @staticmethod
    def analyse(args) -> None:
        analyse(args)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    modes = parser.add_subparsers(dest="command", required=True)

    # run mode
    run_mode = modes.add_parser("run")
    run_mode.set_defaults(func=ModeMapper.run)
    run_mode.add_argument(
        "-m", "--main_input", type=str, default="data/gadm41_CZE.gpkg"
    )
    run_mode.add_argument(
        "-s", "--secondary_input", type=str, default="data/gadm41_SVK.gpkg"
    )
    run_mode.add_argument("-o", "--output_dir", type=str, default="output")

    # analysis mode
    analysis_mode = modes.add_parser("analyse")
    analysis_mode.set_defaults(func=ModeMapper.analyse)
    analysis_mode.add_argument("-v", "--vertices", type=vertex_number, default=10)
    analysis_mode.add_argument(
        "-vi", "--vertex_increment", type=non_negative_int, default=10
    )
    analysis_mode.add_argument("-s", "--shapes", type=positive_int, default=10)
    analysis_mode.add_argument(
        "-si", "--shape_increment", type=non_negative_int, default=10
    )
    analysis_mode.add_argument("-it", "--iterations", type=positive_int, default=20)
    analysis_mode.add_argument("-agg", "--aggregations", type=positive_int, default=5)
    analysis_mode.add_argument("-o", "--output_dir", type=str, default="output")
    analysis_mode.add_argument(
        "-gm", "--generation_mode", choices=FUNCTION_MAPPING.keys(), default="regular"
    )

    arguments = parser.parse_args()
    arguments.func(arguments)
