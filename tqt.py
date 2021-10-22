#!/usr/bin/env python3
"""Text Query Tool (TQT).

TQT implements safe and simple version of some text filtering shell scripts' commands.
It is safe and uniform kind of cat, cut, grep and sed calls and regex handling on the quality level and regex
instruction set of Perl/Python (Perl-compatible regular expressions (PCREs)).
"""
import argparse
import fileinput
import os
import re
import sys

PROG = "tqt.py"
VERSION = "1.1"


class Cat:
  """Concatenate stdin and files and print on the standard output."""

  def __init__(self, files=None) -> None:
    """[TODO summary].

    Args:
        files ([type], optional): [description]. Defaults to None.

    """
    if files:
      for path in files:
        if not os.path.isfile(path):
          raise FileNotFoundError(f"File {path} does not exist.")
    self.files = files

  def concatenate(self) -> None:
    """[TODO summary]."""
    for line in fileinput.input(files=self.files):
      print(line.rstrip())


class Cut(Cat):
  """[TODO summary].

  Args:
      Cat ([type]): [description]

  """

  def __init__(self, files=None, delimiter="\t", fields="0,-1") -> None:
    r"""[TODO summary].

    Args:
        files ([type], optional): [description]. Defaults to None.
        delimiter (str, optional): [description]. Defaults to "\t".
        fields (str, optional): [description]. Defaults to "0,-1".

    """
    super().__init__(files)
    self.delimiter = delimiter
    if not re.match(r"^(None|\d*),(None|\d*)$", fields):
      raise SyntaxError("FIELDS syntax must be <N,M>; where N,M can be nothing, integer, or None.")
    self.fields = fields.split(",")

  def select(self) -> None:
    """[TODO summary].

    First element index: 0
    Last element index: None
    Element before last index: -1; and so on.
    """
    for line in fileinput.input(files=self.files):
      line = line.rstrip()
      field_values = re.split(self.delimiter, line)
      first, last = self.fields
      if first == "" or first == "None":
        first = None
      else:
        first = int(first)
      if last == "" or last == "None":
        last = None
      else:
        last = int(last)
      print(self.delimiter.join(field_values[first:last]))


class Grep(Cat):
  """[TODO summary].

  Args:
      Cat ([type]): [description]

  """

  def __init__(self, files=None, lines="0,-1", regexes=None) -> None:
    """[TODO summary].

    Args:
        files ([type], optional): [description]. Defaults to None.
        lines (str, optional): [description]. Defaults to "0,-1".
        regexes ([type], optional): [description]. Defaults to None.

    """
    super().__init__(files)
    if lines:
      if not re.match(r"^(None|\d*),(None|\d*)$", lines):
        raise SyntaxError("LINES syntax must be <N,M>; where N,M can be nothing, integer, or None.")
    self.lines = lines
    self.regexes = regexes

  def search(self) -> None:
    """[TODO summary]."""
    for i, line in enumerate(fileinput.input(files=self.files)):
      line = line.rstrip()
      in_lines = None
      if self.lines:
        in_lines = self.lines.split(",")
      if in_lines and i < int(in_lines[0]):
        continue
      if in_lines and in_lines[1] != "-1" and i > int(in_lines[1]):  # TODO test this
        break
      for regex in self.regexes:
        if re.search(fr"{regex}", line):
          print(line)
          break


class Sed(Grep):
  """[TODO summary].

  Args:
      Grep ([type]): [description]

  """

  def __init__(self, files=None, lines="0,-1", regexes=None, replacements=None, insert=None, append=None, deletion=None) -> None:
    """[TODO summary].

    Args:
        files ([type], optional): [description]. Defaults to None.
        lines (str, optional): [description]. Defaults to "0,-1".
        regexes ([type], optional): [description]. Defaults to None.
        replacements ([type], optional): [description]. Defaults to None.
        insert ([type], optional): [description]. Defaults to None.
        append ([type], optional): [description]. Defaults to None.
        deletion ([type], optional): [description]. Defaults to None.

    """
    super().__init__(files, lines, regexes)
    if len(regexes) != len(replacements):
      raise IndexError("Number of EXPRESSION(s) and SUBSITUTE(s) must be the same.")
    self.regexes = regexes
    self.replacements = replacements
    self.insert = insert
    self.append = append
    self.deletion = deletion

  def _replace(self) -> None:
    for line in fileinput.input(files=self.files):
      line = line.rstrip()
      from_to = tuple(zip(self.regexes, self.replacements))
      for pattern, repl in from_to:
        if re.search(fr"{pattern}", line):
          print(re.sub(fr"{pattern}", repl, line))
        else:
          print(line)

  def _delete(self) -> None:
    for line in fileinput.input(files=self.files):
      line = line.rstrip()
      if any([re.search(fr"{regex}", line) for regex in self.regexes]):
        print(line)

  def _insert(self) -> None:
    # TODO
    print("Not implemented.")

  def _append(self) -> None:
    # TODO
    print("Not implemented.")

  def edit(self) -> None:
    """[TODO summary]."""
    if self.deletion:
      self._delete()
    elif self.replacements:
      self._replace()
    elif self.append:
      self._append()
    elif self.insert:
      self._insert()


if __name__ == "__main__":
  main_group = argparse.ArgumentParser(prog=PROG, description=__doc__)
  main_group.add_argument("-V", "--version", action="version", version=f"%(prog)s {VERSION}")
  main_group.add_argument("command", help="command to be executed", choices=["cat", "cut", "grep", "sed"])
  main_group.add_argument("-f", "--file", action="extend", nargs="+", help="add file(s) to be examined (default: stdin)")
  main_group.add_argument("-l", "--lines", help="select LINES range <N,M> [0,-1]")
  main_group.add_argument("-e", "--expression", action="extend", nargs="+", help="select regex EXPRESSION(s) matching")
  cut_group = main_group.add_argument_group("cut arguments")
  cut_group.add_argument("-D", "--delimiter", help="set regex DELIMITER for field separation")
  cut_group.add_argument("-F", "--fields", help="select FIELDS <N,M> [0,-1]")
  grep_group = main_group.add_argument_group("grep arguments")
  grep_group.add_argument("-c", "--ignore-case", action="store_true", help="ignore case distinctions")
  grep_group.add_argument("-v", "--invert-match", action="store_true", help="select non-matching lines")
  sed_group = main_group.add_argument_group("sed arguments")
  sed_options = sed_group.add_mutually_exclusive_group()
  sed_options.add_argument("-s", "--substitute", action="extend", nargs="+", help="replace to SUBSITUTE(s)")
  sed_options.add_argument("-i", "--insert", help="insert INSERT string before")
  sed_options.add_argument("-a", "--append", help="append APPEND string after")
  sed_options.add_argument("-d", "--delete", action="store_true", help="delete selected lines")
  args = main_group.parse_args()
  sys.argv.remove(args.command)

  if args.command == "cat":
    Cat(args.file).concatenate()
  elif args.command == "cut":
    Cut(args.file, args.delimiter, args.fields).select()
  elif args.command == "grep":
    Grep(args.file, args.lines, args.expression).search()
  elif args.command == "sed":
    Sed(args.file, args.lines, args.expression, args.substitute, args.insert, args.append, args.delete).edit()
