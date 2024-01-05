import argparse

from app import plotter


class ModeMapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def run(args) -> None:
        plotter()

    @staticmethod
    def test(args) -> None:
        plotter()


if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    modes = parser.add_subparsers(dest="command", required=True)

    # run mode
    run_mode = modes.add_parser("run")
    run_mode.set_defaults(func=ModeMapper.run)

    # test mode
    test_mode = modes.add_parser("test")
    test_mode.set_defaults(func=ModeMapper.test)

    arguments = parser.parse_args()
    arguments.func(arguments)
