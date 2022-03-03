# snip-tsv

Crop tabular data files

## Installation

```bash
pip install snip-tsv
```

## Usage

```text
$ snip -h
usage: snip [-h] [-v] [-H] [-d DELIMITER] [-x PLOT_X] [-y PLOT_Y]
            [-c CROP_COL] [-s CROP_START] [-e CROP_END]
            [-o OUT_FILE]
            in_file

positional arguments:
  in_file               Input data file. (default: -)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -H, --header          When set assume the first row to be a
                        header row. By default, no header row is
                        assumed.
  -d DELIMITER, --delimiter DELIMITER
                        The delimiter used in the input data file.
                        (default: '\t')
  -x PLOT_X, --plot-x PLOT_X
                        Column to use on the x-axis. A 0-indexed
                        integer or a column heading string.
                        (default: 0)
  -y PLOT_Y, --plot-y PLOT_Y
                        Column to use on the y-axis. A 0-indexed
                        integer or a column heading string.
                        (default: 1)
  -c CROP_COL, --crop-col CROP_COL
                        Column to search in for --crop-
                        start/--crop-end values. A 0-indexed
                        integer or a column heading string.
                        (default: 0)
  -s CROP_START, --crop-start CROP_START
                        Start value to use for cropping
                        (inclusive). If the column is numeric then
                        the row with column entry closest to the
                        given value is used.
  -e CROP_END, --crop-end CROP_END
                        End value to use for cropping (exclusive).
                        If the column is numeric then the row with
                        column entry closest to the given value is
                        used. To specify a numeric value relative
                        to --crop-start use the syntax ':<number>'.
                        Omit this flag to crop from --crop-start to
                        the end of the file.
  -o OUT_FILE, --out-file OUT_FILE
                        File to write the results to (either an
                        image or TSV file. If not provided a
                        matplotlib plot is shown when plotting, and
                        data is written to stdout when cropping.
                        (default: -)
```
