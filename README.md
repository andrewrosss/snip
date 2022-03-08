# snip-tsv

Crop tabular data files

## Installation

```bash
pip install snip-tsv
```

## Usage

```text
$ snip -h
usage: snip [-h] [-v] [-H] [-d DELIMITER] [-o OUT_FILE] [-x PLOT_X]
            [-y PLOT_Y] [-s START] [-e END] [-c COL]
            [-p PICK | -r OMIT]
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
  -o OUT_FILE, --out-file OUT_FILE
                        File to write the results to (either an
                        image or TSV file. If not provided, a
                        matplotlib plot is shown when plotting, and
                        data is written to stdout when cropping.
                        (default: -)

plot options:
  -x PLOT_X, --plot-x PLOT_X
                        Column to use on the x-axis. A 0-indexed
                        integer or a column heading string.
                        (default: 0)
  -y PLOT_Y, --plot-y PLOT_Y
                        Column to use on the y-axis. A 0-indexed
                        integer or a column heading string.
                        (default: 1)

crop options:
  -s START, --start START
                        Start value to use for cropping
                        (inclusive). If the column is numeric then
                        the row with column entry closest to the
                        given value is used.
  -e END, --end END     End value to use for cropping (exclusive).
                        If the column is numeric then the row with
                        column entry closest to the given value is
                        used. To specify a numeric value relative
                        to --crop-start use the syntax ':<number>'.
                        Omit this flag to crop from --crop-start to
                        the end of the file.
  -c COL, --col COL     Column to search in for --crop-
                        start/--crop-end values. A 0-indexed
                        integer or a column heading string.
                        (default: 0)
  -p PICK, --pick PICK  Comma separated list of columns to keep. If
                        specified, only columns in this list will
                        appear in the generated output. Columns can
                        either be column heading strings or
                        0-indexed integers (intermixing is
                        allowed). By default all columns are
                        retained.
  -r OMIT, --omit OMIT  Comma separated list of columns to omit. If
                        specified, columns in this list will be
                        removed from the generated output. Columns
                        can either be column heading strings or
                        0-indexed integers (intermixing is
                        allowed).
```
