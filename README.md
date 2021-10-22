# Text Query Tool (TQT)

TQT implements safe and simple version of some text filtering shell scripts' commands.
It is safe and uniform kind of cat, cut, grep and sed calls and regex handling on the quality level and regex
instruction set of Perl/Python (Perl-compatible regular expressions (PCREs)).

## Usage

```text
usage: tqt.py [-h] [-V] [-f FILE [FILE ...]] [-l LINES] [-e EXPRESSION [EXPRESSION ...]] [-D DELIMITER] [-F FIELDS] [-c] [-v] [-s SUBSTITUTE [SUBSTITUTE ...] | -i INSERT |
              -a APPEND | -d]
              {cat,cut,grep,sed}

Text Query Tool (TQT). TQT implements safe and simple version of some text filtering shell scripts' commands. It is safe and uniform kind of cat, cut, grep and sed calls and
regex handling on the quality level and regex instruction set of Perl/Python (Perl-compatible regular expressions (PCREs)).

positional arguments:
  {cat,cut,grep,sed}    command to be executed

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -f FILE [FILE ...], --file FILE [FILE ...]
                        add file(s) to be examined (default: stdin)
  -l LINES, --lines LINES
                        select LINES range <N,M> [0,-1]
  -e EXPRESSION [EXPRESSION ...], --expression EXPRESSION [EXPRESSION ...]
                        select regex EXPRESSION(s) matching

cut arguments:
  -D DELIMITER, --delimiter DELIMITER
                        set regex DELIMITER for field separation
  -F FIELDS, --fields FIELDS
                        select FIELDS <N,M> [0,-1]

grep arguments:
  -c, --ignore-case     ignore case distinctions
  -v, --invert-match    select non-matching lines

sed arguments:
  -s SUBSTITUTE [SUBSTITUTE ...], --substitute SUBSTITUTE [SUBSTITUTE ...]
                        replace to SUBSITUTE(s)
  -i INSERT, --insert INSERT
                        insert INSERT string before
  -a APPEND, --append APPEND
                        append APPEND string after
  -d, --delete          delete selected lines
```
