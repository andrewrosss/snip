from __future__ import annotations

import argparse
import ast
import csv
from io import TextIOWrapper
from typing import Any
from typing import NamedTuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


__version__ = "0.3.0"


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
    has_header: bool = args.header
    delimiter: str = args.delimiter
    popts = PlotOptions.from_namespace(args)
    copts = CropOptions.from_namespace(args)
    out_file: TextIOWrapper = args.out_file

    data = read_file(in_file, delimiter, has_header)

    if copts.start is not None:
        cropped_data = crop(data, copts)
        return write_records(cropped_data, out_file, delimiter)
    else:
        fig, ax = plot(data, popts)
        return write_figure(fig, ax, out_file)


class CropOptions(NamedTuple):
    col: int
    start: Any
    end: Any

    @classmethod
    def from_namespace(cls, args: argparse.Namespace):
        return cls(args.crop_col, coerce(args.crop_start), coerce(args.crop_end))


class PlotOptions(NamedTuple):
    x: int = Defaults.PLOT_X
    y: int = Defaults.PLOT_Y

    @classmethod
    def from_namespace(cls, args: argparse.Namespace):
        return cls(args.plot_x, args.plot_y)


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


class Data(NamedTuple):
    records: list[list[Any]]
    header: list[Any] | None = None
    filename: str | None = None
    is_numeric: list[bool] | None = None


def read_file(
    file: TextIOWrapper,
    delimiter: str = Defaults.DELIMITER,
    has_header: bool = Defaults.HEADER,
) -> Data:
    reader = csv.reader(file, delimiter=delimiter)
    header = next(reader) if has_header else None
    records = [[coerce(c) for c in row] for row in reader]
    is_numeric = _determine_numeric_columns(records)
    return Data(records, header, file.name, is_numeric)


def _determine_numeric_columns(records: list[list[Any]]) -> list[bool]:
    is_numeric = [True for _ in records[0]]
    for record in records:
        is_numeric = [
            is_num and isinstance(entry, (int, float))
            for is_num, entry in zip(is_numeric, record)
        ]
    return is_numeric


def crop(data: Data, opts: CropOptions) -> Data:
    start_idx: int | None = None
    end_idx: int | None = None
    for i, record in enumerate(data.records):
        if record[opts.col] == opts.start and start_idx is None:
            start_idx = i
        if opts.end is not None and record[opts.col] == opts.end and end_idx is None:
            end_idx = i

    return Data(data.records[start_idx:end_idx], data.header, data.filename)


def write_records(
    data: Data,
    out_file: TextIOWrapper,
    delimiter: str = Defaults.DELIMITER,
) -> int:
    writer = csv.writer(out_file, delimiter=delimiter)
    if data.header is not None:
        writer.writerow(data.header)
    writer.writerows(data.records)

    return 0


def plot(data: Data, opts: PlotOptions) -> tuple[Figure, Axes]:
    fig, ax = plt.subplots()
    x = [r[opts.x] for r in data.records]
    y = [r[opts.y] for r in data.records]
    ax.plot(x, y)

    return fig, ax


def write_figure(fig: Figure, ax: Axes, out_file: TextIOWrapper) -> int:
    if out_file.name in ("<stdout>", "<stderr>"):
        plt.show()
    else:
        fig.savefig(out_file.name, dpi=200)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
