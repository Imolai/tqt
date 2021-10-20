#!/usr/bin/env python3
import os
import subprocess
import unittest


def run(cmd):
  p = subprocess.run(cmd, shell=True, capture_output=True)
  return (p.returncode, p.stdout.decode('utf-8').rstrip(), p.stderr.decode('utf-8').rstrip())


class TestSafeSh(unittest.TestCase):
  def setUp(self):
    self.cmd = "./safesh.py"
    self.testfile = "./testfile_safesh.txt"
    self.testfile_py = "./testfile_safesh.py"
    self.testfile_text = r"""# comment
# lines
"
Hola,
Hello
,
helloooo,
World
!
"
"""
    self.testfile_python = r"""
    #!/usr/bin/env python3
from datetime import date

d = date.fromisoformat("2021-10-20")
print(f"{d.year}/{d.month}/{d.day}")
"""
    with open(self.testfile, "w") as f:
      f.write(self.testfile_text)
    with open(self.testfile_py, "w") as f:
      f.write(self.testfile_python)

  def tearDown(self):
    if os.path.isfile(self.testfile):
      os.remove(self.testfile)
    if os.path.isfile(self.testfile_py):
      os.remove(self.testfile_py)

  def test_blank(self):
    rc, _, err = run(f"{self.cmd}")
    self.assertEqual(rc, 2)
    self.assertRegex(err, r'error: the following arguments are required: command')

  def test_help(self):
    rc, out, _ = run(f"{self.cmd} -h")
    self.assertEqual(rc, 0)
    self.assertRegex(out, r'usage: safesh\.py .[-]h. .[-]f FILE. .[-]e EXPRESSION')

  def test_wrong_command(self):
    rc, _, err = run(f"{self.cmd} undefined")
    self.assertEqual(rc, 1)
    self.assertRegex(err, r'SyntaxError: command to be executed has to be <cat\|grep\|sed>')

  def test_wrong_argument(self):
    rc, _, err = run(f"{self.cmd} cat {self.testfile}")
    self.assertEqual(rc, 2)
    self.assertRegex(err, r'error: unrecognized arguments:')

  def test_cat_stdin(self):
    rc, out, _ = run(f"{self.cmd} cat < {self.testfile}")
    self.assertEqual(rc, 0)
    self.assertRegex(out, r'Hello\n,\nhelloooo,\nWorld')

  def test_cat_f(self):
    rc, out, _ = run(f"{self.cmd} cat -f {self.testfile}")
    self.assertEqual(rc, 0)
    self.assertRegex(out, r'Hello\n,\nhelloooo,\nWorld')

  def test_cat_file(self):
    rc, out, _ = run(f"{self.cmd} cat --file {self.testfile}")
    self.assertEqual(rc, 0)
    self.assertRegex(out, r'Hello\n,\nhelloooo,\nWorld')

  def test_cat_ff(self):
    rc, out, _ = run(f"{self.cmd} cat -f {self.testfile} -f {self.testfile_py}")
    self.assertEqual(rc, 0)
    self.assertRegex(out, r'Hello\n,\nhelloooo,\nWorld')
    self.assertRegex(out, r'#!/usr/bin/env python3\nfrom datetime import date')

  def test_cat_file_file(self):
    rc, out, _ = run(f"{self.cmd} cat --file {self.testfile} --file {self.testfile_py}")
    self.assertEqual(rc, 0)
    self.assertRegex(out, r'Hello\n,\nhelloooo,\nWorld')
    self.assertRegex(out, r'#!/usr/bin/env python3\nfrom datetime import date')


if __name__ == '__main__':
  unittest.main(verbosity=2)
