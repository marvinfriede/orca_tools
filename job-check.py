#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
import argparse
from pathlib import Path

try:
  import pandas as pd
except ModuleNotFoundError:
  sys.exit("Module 'pandas' not installed. Exiting.")

try:
  import numpy as np
except ModuleNotFoundError:
  sys.exit("Module 'numpy' not installed. Exiting.")


orca = {
  "conv_error_str": "NOT FULLY CONVERGED",
  "multijob_pos": 3,
  "multijob_str": "^\$ THERE ARE \d* JOBS TO BE PROCESSED THIS RUN \$$",
  "out_file": "orca",
  "scf_str": "SCF CONVERGED AFTER"
}

qchem = {
  "conv_error_str": "False",
  "multijob_pos": -1,
  "multijob_str": "^User input: \d of \d*$",
  "out_file": "job",
  "scf_str": "Convergence criterion met"
}


def initArgparser():
  parser = argparse.ArgumentParser(
      description='Check all files for successful run.')
  parser.add_argument("-v", '--verbose', nargs='?', const=0, type=int,
                      help="Print more. Number of rows optional. 0 prints everything")
  return parser.parse_args()


def isConverged(prog, file):
  # init variables
  count_criter = 0
  num_jobs = 1

  with open(file) as f:
    for line in f:
      # get number of jobs in multijob file
      if re.match(prog["multijob_str"], line.strip()):
        pos = prog["multijob_pos"]
        num_jobs = int(line.strip().split()[pos])
        continue

      if prog["scf_str"] in line:
        count_criter += 1
        continue

      if prog["conv_error_str"] in line:
        return False

    # check convergence for multijob
    if count_criter != num_jobs:
      return False

  return True


def main():
  args = initArgparser()

  # init variables
  failed = []
  success = []

  # compile filelist
  out_file_names = [orca["out_file"], qchem["out_file"]]
  filelist, lenFileList = getFileList(out_file_names)

  # iterate filelist
  for i, path in enumerate(filelist):
    # ORCA files
    if re.match(fr"{orca['out_file']}.*\.out", path.name):
      status = isConverged(orca, path)

    # Q-CHEM files
    elif re.match(fr"{qchem['out_file']}.*\.out", path.name):
      status = isConverged(qchem, path)

    # unrecognized files
    else:
      print(f"File '{path}' not recognized.")
      status = False

    if status:
      success.append(path)
    else:
      failed.append(path)


    # pretty progress bar
    progress(i+1, lenFileList)


  print("\nFinished!\n")
  if len(failed) == 0:
    print("All jobs successful!!")
  else:
    print(f"Only {len(success)}/{lenFileList} calculations converged:")
    [print(i) for i in success]

    print(f"\nConvergence not reached in {len(failed)}/{lenFileList}:")
    [print(i) for i in failed]
  

def getFileList(out_file_names):
  filelist = []

  print("Compiling file list...", end =" ")
  for name in out_file_names:
    for file in sorted(Path(".").rglob(f"{name}*.out")):
      filelist.append(file)

  if len(filelist) == 0:
    sys.exit("No '.out' files found.")

  lenFileList = len(filelist)
  print(f"{lenFileList} files found.")

  return filelist, lenFileList


def progress(count, total, status=''):
  bar_len = 60
  filled_len = int(round(bar_len * count / float(total)))

  percents = round(100.0 * count / float(total), 1)
  bar = '=' * filled_len + '-' * (bar_len - filled_len)

  sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
  sys.stdout.flush()


if __name__ == '__main__':
  main()
