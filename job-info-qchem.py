#!/usr/bin/env python3
# coding: utf-8

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
  "scf_str": "SCF CONVERGED AFTER",
  "time_str": "TOTAL RUN TIME:"
}

qchem = {
  "conv_error_str": "False",
  "multijob_pos": -1,
  "multijob_str": "^User input: \d of \d*$",
  "nbas_str": "^There are \d* shells and \d* basis functions$",
  "nbas_num_str": "^There are \d* shells and (\d*) basis functions$",
  "out_file": "job",
  "scf_str": "Convergence criterion met",
  "time_str": "SCF time:   CPU",
  "time_pos": -1
}


def main():
  args = initArgparser()

  # init variables
  failed = []
  data = []

  # compile filelist
  out_file_names = [qchem["out_file"]]
  filelist, lenFileList = getFileList(out_file_names)

  for i, path in enumerate(filelist):
    # ORCA files
    if re.match(fr"{orca['out_file']}.*\.out", path.name):
      info, rem_dict = handleFile(orca, path)

    # Q-CHEM files
    elif re.match(fr"{qchem['out_file']}.*\.out", path.name):
      info, rem_dict = handleFile(qchem, path)

    # unrecognized files
    else:
      print(f"File '{path}' not recognized.")
      info = False


    progress(i+1, len(filelist))

  print(info)
  print("\nFinished!\n")
  if len(failed) == 0:
    print("All jobs successful!!")
  else:
    print("WARNING!!! Convergence not reached in:")
    for i in failed:
      print(i)

  ########################################
  ## data collection (outside of loop!) ##
  ########################################

  cols = ["filename", "energy", "nbas", "time"] + list(rem_dict.keys())
  df = pd.DataFrame(columns=cols, data=info)

  # print to console
  if args.verbose is not None:
    if args.verbose == 0:
      pd.set_option('display.max_rows', df.shape[0] + 1)
      print(df)
    else:
      print(df.head(args.verbose))
  else:
    print(df)

  # save
  if args.save:
    save_loc = os.path.join(os.path.realpath("."), args.save)
    df.to_csv(save_loc, index=False)
    print("\nSaved data to {}.".format(save_loc))


def initArgparser():
  parser = argparse.ArgumentParser(
      description='JOB INFO\nSearch recursively for all .out files and get general info.')
  parser.add_argument("-v", '--verbose', nargs='?', const=0, type=int,
                      help="Print more. Number of rows optional. 0 prints everything")
  parser.add_argument("-s", "--save", nargs='?', const="data.csv", type=str,
                      help="Save output. Name is optional. Defaults to 'data.csv'.")
  return parser.parse_args()


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


def handleFile(prog, path):
  rem = False
  rem_dict = {}
  count_criter = 0
  num_jobs = 1
  failed = []
  data = []

  with open(path) as f:
    for line in f:
      line = line.strip()

      # only entered if previous line was start of rem block
      if rem is True:
        # turn false again if end encountered, otherwise do stuff
        if line.startswith("$end"):
          rem = False
        else:
          rem_dict[line.split()[0]] = line.split()[1]

      # turns true if rem block is hit
      if line.startswith("$rem"):
        rem = True

      # get number of jobs in multijob file
      elif re.match(prog["multijob_str"], line):
        pos = prog["multijob_pos"]
        num_jobs = int(line.split()[pos])

      # check SCF convergence
      elif prog["scf_str"] in line:
        count_criter += 1

      # number of basis functions
      elif re.match(prog["nbas_str"], line):
        nbas = re.search(prog["nbas_num_str"], line).group(1)

      elif prog["time_str"] in line:
        pos = prog["time_pos"]
        walltime = line.split()[pos]
        walltime = walltime[:-1]

      # append data in line furthest down
      elif "Total energy in the final basis set =" in line:
        energy = line.split("=")[1]

        # THIS IS A HOT FIX!!
        # first job has no scf guess -> first list shorter
        if "scf_guess" not in rem_dict:
          rem_dict["scf_guess"] = "default"

        # append everything and stop going through file
        data.append([path, energy, nbas, walltime] +
                    list(rem_dict.values()))
        continue

    # check convergence for my multijob
    if count_criter != num_jobs:
      failed.append(path)

  return data, rem_dict


def progress(count, total, status=''):
  bar_len = 60
  filled_len = int(round(bar_len * count / float(total)))

  percents = round(100.0 * count / float(total), 1)
  bar = '=' * filled_len + '-' * (bar_len - filled_len)

  sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
  sys.stdout.flush()


if __name__ == '__main__':
  main()
