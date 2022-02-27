from __future__ import annotations

import argparse
import ast
import csv
from io import TextIOWrapper
from typing import Any

import matplotlib.pyplot as plt


__version__ = "0.1.0"


COL_DTYPE = {"int": int, "float": float, "str": str}


class Defaults:
    IN_FILE = "-"
    DELIMITER = "\t"
    HEADER = False
    PLOT_X = 0
    PLOT_Y = 1
    CROP_COL = 0
    OUT_FILE = "-"


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if hasattr(args, "handler"):
        return args.handler(args)

    parser.print_help()
    return 1


def create_parser(
    parser: argparse.ArgumentParser | None = None,
) -> argparse.ArgumentParser:
    _parser = parser or argparse.ArgumentParser()

    _parser.add_argument(
        "in_file",
        type=argparse.FileType("r"),
        default=Defaults.IN_FILE,
        help="Input data file. (default: %(default)s)",
    )

    _parser.add_argument("-v", "--version", action="version", version=__version__)
    _parser.add_argument(
        "--header",
        default=Defaults.HEADER,
        action="store_true",
        help="When set assume the first row to be a header row. By default, "
        "no header row is assumed.",
    )
    _parser.add_argument(
        "-d",
        "--delimiter",
        default=Defaults.DELIMITER,
        help="The delimiter used in the input data file. (default: %(default)r)",
    )
    _parser.add_argument(
        "-x",
        "--plot-x",
        type=int,
        default=Defaults.PLOT_X,
        help="Column to use on the x-axis. A 0-indexed integer. (default: %(default)s)",
    )
    _parser.add_argument(
        "-y",
        "--plot-y",
        type=int,
        default=Defaults.PLOT_Y,
        help="Column to use on the y-axis. A 0-indexed integer. (default: %(default)s)",
    )
    _parser.add_argument(
        "-c",
        "--crop-col",
        type=int,
        default=Defaults.CROP_COL,
        help="Column to search in for --crop-start/--crop-end values. A "
        "0-indexed integer. (default: %(default)s)",
    )
    _parser.add_argument(
        "-s",
        "--crop-start",
        help="Start value to use for cropping (inclusive)",
    )
    _parser.add_argument(
        "-e",
        "--crop-end",
        help="End value to use for cropping (exclusive). Omit this flag to "
        "crop from --crop-start to the end of the file.",
    )
    _parser.add_argument(
        "-o",
        "--out-file",
        type=argparse.FileType("w"),
        default=Defaults.OUT_FILE,
        help="File to write the results to (either an image or TSV file. If "
        "not provided a matplotlib plot is shown when plotting, and data is "
        "written to stdout when cropping. (default: %(default)s)",
    )

    _parser.set_defaults(handler=handler)

    return _parser


def handler(args: argparse.Namespace) -> int:
    in_file: TextIOWrapper = args.in_file
    header: bool = args.header
    delimiter: str = args.delimiter
    plot_x: int = args.plot_x
    plot_y: int = args.plot_y
    crop_col: int = args.crop_col
    crop_start: Any = coerce(args.crop_start)
    crop_end: Any = coerce(args.crop_end)
    out_file: TextIOWrapper = args.out_file

    records = read_file(in_file, delimiter, header)

    if crop_start is not None:
        cropped_records = crop(records, crop_col, crop_start, crop_end)
        return write_records(cropped_records, out_file, delimiter)
    else:
        return plot(records, out_file, plot_x, plot_y)


def coerce(s: str | None) -> Any:
    if s is None:
        return s
    try:
        return ast.literal_eval(s)
    except SyntaxError:
        return ast.literal_eval(f"'{s}'")
    except ValueError:
        if s.lower() == "nan":
            return float(s)
        raise


def read_file(
    file: TextIOWrapper,
    delimiter: str = Defaults.DELIMITER,
    header: bool = Defaults.HEADER,
) -> list[list[Any]]:
    reader = csv.reader(file, delimiter=delimiter)
    if header:
        next(reader)
    return [[coerce(c) for c in row] for row in reader]


def crop(records: list[list[Any]], col: int, start: Any, end: Any) -> list[list[Any]]:
    start_idx: int | None = None
    end_idx: int | None = None
    for i, record in enumerate(records):
        if record[col] == start and start_idx is None:
            start_idx = i
        if end is not None and record[col] == end and end_idx is None:
            end_idx = i

    return records[start_idx:end_idx]


def write_records(
    records: list[list[str]],
    out_file: TextIOWrapper,
    delimiter: str = Defaults.DELIMITER,
) -> int:
    writer = csv.writer(out_file, delimiter=delimiter)
    writer.writerows(records)
    return 0


def plot(
    records: list[list[str]],
    out_file: TextIOWrapper,
    plot_x: int = Defaults.PLOT_X,
    plot_y: int = Defaults.PLOT_Y,
) -> int:
    fig, ax = plt.subplots()
    x = [r[plot_x] for r in records]
    y = [r[plot_y] for r in records]
    ax.plot(x, y)

    if out_file.name in ("<stdout>", "<stderr>"):
        plt.show()
    else:
        fig.savefig(out_file.name, dpi=200)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
