#!/usr/bin/env python3
"""Implement safe and simple version of shell scripts' commands.

Base idea comes from I want a safe and uniform kind of grep and sed regex handling on the quality level and regex
instruction set of Perl.
"""
import argparse
import fileinput
import re
import sys


class Cat:
  """Concatenate stdin and files and print on the standard output."""

  def __init__(self, files=None) -> None:
    self.files = files

  def concatenate(self) -> None:
    for line in fileinput.input(files=self.files):
      print(line.rstrip())


class Grep(Cat):
  def __init__(self, files=None, regexes=None) -> None:
    self.files = files
    self.regexes = regexes

  def search(self) -> None:
    for line in fileinput.input(files=self.files):
      line = line.rstrip()
      for regex in self.regexes:
        if re.search(fr"{regex}", line):
          print(line)
          break


class Sed(Grep):
  def __init__(self, files=None, regexes=None, replacement=None, deletion=None) -> None:
    self.files = files
    self.regex = regexes[0]
    self.replacement = replacement
    self.deletion = deletion

  def _replace(self) -> None:
    for line in fileinput.input(files=self.files):
      line = line.rstrip()
      if re.search(fr"{self.regex}", line):
        print(re.sub(fr"{self.regex}", self.replacement, line))
      else:
        print(line)

  def _delete(self) -> None:
    for line in fileinput.input(files=self.files):
      line = line.rstrip()
      if not re.search(fr"{self.regex}", line):
        print(line)

  def do(self) -> None:
    if self.deletion:
      self._delete()
    elif self.replacement:
      self._replace()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("command", help="command to be executed <cat|grep|sed>")
  parser.add_argument("-f", "--file", action="append", help="file(s) to be examined")
  parser.add_argument("-e", "--expression", action="append", help="regexs(s) to be matched")
  parser.add_argument("-r", "--replacement", help="replace to this string")
  parser.add_argument("-d", "--delete", action='store_true', help="delete these lines")
  args = parser.parse_args()
  if args.command not in ("cat", "grep", "sed"):
    raise SyntaxError("command to be executed has to be <cat|grep|sed>")
  sys.argv.remove(args.command)
  if args.file:
    while "-f" in sys.argv:
      sys.argv.remove("-f")
    for f in args.file:
      sys.argv.remove(f)
  if args.expression:
    while "-e" in sys.argv:
      sys.argv.remove("-e")
    for e in args.expression:
      sys.argv.remove(e)
  if args.replacement:
    sys.argv.remove("-r")
    sys.argv.remove(args.replacement)
  if args.delete:
    sys.argv.remove("-d")

  if args.command == 'cat':
    Cat(args.file).concatenate()
  elif args.command == 'grep':
    Grep(args.file, args.expression).search()
  elif args.command == 'sed':
    Sed(args.file, args.expression, args.replacement, args.delete).do()
