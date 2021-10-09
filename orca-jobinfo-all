#!/usr/bin/env python3
# coding: utf-8

import time
import glob
import os
import sys
import pandas as pd


def main():
  data = []
  funclist = ["b3lyp", "bp", "pbe", "tpss", "tpssh", "pbe0", "bp86",
              "blyp", "lda", "bhlyp", "b2plyp", "cam-b3lyp", "m06-2x",
              "pw6b95", "pbeh-3c", "b97-3c", "dsd-pbep86", "pw6b95"]

  filelist = getFileList()
  for filename in filelist:
    earlycrash = "unset"
    xyzfileerror = "unset"
    runcomplete = "unset"
    orcacrash = "unset"
    conbf = "unset"
    cpscferror = "unset"
    scferrorgeneral = "unset"
    scfstillrunning = "unset"
    scfalmostconv = "unset"
    parproc = "unset"
    jobtype = "unset"
    scfmethod = "unset"
    dft = "unset"
    optrunconverged = "unset"
    linearcheck = "unset"
    optenergy = "unset"
    finaltopenergy = "unset"
    opterror = "unset"
    optnotconv = "unset"
    optcycle = "unset"
    intelectrons = "unset"
    freqjob = "unset"
    freqsection = "unset"
    freqsearch = "unset"
    optjob = "unset"
    scfconv = "unset"
    noiter = "unset"
    moread = "unset"
    autostart = "unset"
    postHFmethod = "unset"
    postHF = "unset"
    frozel = "unset"
    correl = "unset"
    refenergy = "unset"
    correnergy = "unset"
    caseinputline = "unset"
    inputline = "unset"
    nofrozencore = "unset"
    casscf = "unset"
    lastmacroiter = "unset"
    casscfconv = "unset"
    nevpt2correnergy = "unset"
    version = "unset"
    semiempirical = "unset"
    functional = "unknown"
    engrad = "unset"
    freqinrun = "unset"
    charge = "unset"
    endofinput = "unset"
    numatoms = "unset"
    spin = "unset"
    actualelec = "unset"
    temprcount = "unset"
    diagerror = "unset"
    brokensym = "unset"
    flipspin = "unset"
    errormult = "unset"
    scfcycleslist = []
    errormessage = []
    s2value = "unset"
    ideals2value = "unset"
    scftype = "unset"
    occorbsgrab = "unset"
    virtorbsgrab = "unset"
    orbs = []
    lastvirt_a = "unset"
    lastocc_a = "unset"
    gap_a = "unset"
    spsection = "unset"
    optsection = "unset"
    finalgeo = "unset"
    coord = "unset"
    geomconvtable = "unset"
    geomconvgrab = "unset"
    lastgeomark = "unset"
    numatomcountstart = "unset"
    scantest = "unset"
    findenergy = "unset"
    scanenergies = []
    scanoptcycle = []
    lastscanoptcycle = "unset"
    lastenergy = "unset"
    allscanstepnums = []
    bsenergies = []
    rctype = "unset"
    scanatomA = "unset"
    scanatomB = "unset"
    scanatomC = "unset"
    scanatomD = "unset"
    extrapolate = "unset"
    extrapscfenergy = "unset"
    extrapcorrenergy = "unset"
    basissets = []
    newjob = "unset"
    finalsingleline = "unset"
    imaginmodes = []
    atomcoord = []
    optgeo = []
    lastgeo = []
    inputgeo = []
    geomconv = []
    rmsgradlist = []
    grabsimpleinput = False
    count = 0
    case = ''
    method = "unset"
    with open(filename, errors='ignore') as f:
      for line in f:
        count = count + 1

        # get the input line
        if caseinputline == "unset":
          if grabsimpleinput is True:
            if '!' in line and not '#' in line:
              var1 = line.lower().split()[2:]
              var2 = ' '.join(var1)
              var2 = var2.replace("!", " ")
              case = case+var2 + " "
              print(case)
          else:
            if grabsimpleinput is False and 'INPUT FILE' in line:
              grabsimpleinput = True

        # Here checking for stuff in listed inputfile until 'END OF INPUT'
        if endofinput == "unset":
          if 'END OF INPUT' in line:
            endofinput = "yes"
            grabsimpleinput = False
            caseinputline = case
            # Now going through simple-input keywords here to determine job-type
            if caseinputline != "unset":

              # Checking for method
              for i in funclist:
                if i in caseinputline:
                  method = i

              if method == "unset":
                if "ccsd" in caseinputline:
                  method = "ccsd"
                elif "mp2" in caseinputline:
                  method = "mp2"
                elif "qcisd" in caseinputline:
                  method = "yes"
                elif "ccsdt" in caseinputline:
                  method = "CC"
                elif "cisd" in caseinputline:
                  method = "cisdt"
                elif "ccsd(t)" in caseinputline:
                  method = "ccsd(t)"
                elif "dlpno-ccsd(t)" in caseinputline:
                  method = "dlpno-ccsd(t)"
                else:
                  method = ""

              # check jobtype
              if "extrapolate" in caseinputline:
                extrapolate = "yes"
              # Checking for opt or freq here
              if " optts " in caseinputline or " optts\n" in caseinputline:
                jobtype = "optts"
              elif " freq " in caseinputline or " numfreq " in caseinputline or " freq" in caseinputline or " numfreq" in caseinputline:
                jobtype = "opttsfreq"
                freqsection = "notyetdone"
              elif " opt" in caseinputline or " tightopt" in caseinputline or "copt" in caseinputline:
                jobtype = "opt"
                # print("jobtype is", jobtype)
                if " freq" in caseinputline or " numfreq" in caseinputline:
                  jobtype = "optfreq"
                  freqsection = "notyetdone"
              elif " md " in caseinputline:
                jobtype = "md"
              elif " freq " in caseinputline:
                jobtype = "freqsp"
                freqsection = "notyetdone"
              elif " engrad " in caseinputline:
                jobtype = "sp"
                engrad = "yes"
              else:
                jobtype = "sp"

          # Going through block input
          if casscf == "unset":
            if '%casscf' in line:
              method = "casscf"

        if endofinput == "yes":
          # get number of basis functions
          if conbf == "unset" and semiempirical == "unset":
            if '# of contracted basis functions' in line:
              conbf = line.split()[-1]
            if 'Number of basis functions' in line:
              conbf = line.split()[5]
            if casscf == "yes":
              if 'Number of basis functions' in line:
                conbf = line.split()[5]

        # Finding parallel and SCF output after basis output
        if conbf != "unset" or semiempirical == "yes":
          if parproc == "unset":
            if 'parallel MPI-processes' in line:
              parproc = line.split()[4]

          # Charge and spin
          if ' Total Charge           Charge' in line:
            charge = line.split()[4]
          if charge != "unset":
            if ' Multiplicity           Mult            ....' in line:
              mult = int(line.split()[3])
              spin = (mult-1)/2.0
            if 'Number of Electrons    NEL             ....' in line:
              actualelec = line.split()[5]
            if 'Nuclear Repulsion      ENuc' in line:
              nucrepuls = line.split()[5]
              break

    if parproc == "unset":
      parproc = 1

    rcount = 0
    with open(filename, errors='ignore') as file:
      for line in reverse_lines(file):
        rcount = rcount+1
        # Error messages. Only last 50 lines checked
        if rcount < 60:
          if 'ERROR: Unknown identifier' in line:
            earlycrash = "yes"
            orcacrash = "yes"
            errormessage.append(line)
          if 'Error (ORCA/TRAFO/RI-GIAO):' in line:
            orcacrash = "yes"
            errormessage.append(line)
          if 'Zero distance between atoms' in line:
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Cannot open input file:' in line:
            orcacrash = "yes"
            earlycrash = "yes"
          if 'You must have a' in line:
            orcacrash = "yes"
            earlycrash = "yes"
          if 'INPUT ERROR' in line:
            inputerror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'ERROR CODE RETURNED FROM CP-SCF PROGRAM' in line:
            cpscferror = "yes"
            orcacrash = "yes"
          if 'ABORTING THE RUN' in line:
            abortcode = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Invalid assignment in' in line:
            abortcode = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Aborting the run' in line:
            abortcode2 = "yes"
            orcacrash = "yes"
          if 'Skipping actual calculation' in line:
            abortcode3 = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Error : multiplicity' in line:
            errormult = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Unrecognized symbol in' in line:
            orcacrash = "yes"
            earlycrash = "yes"
            errormessage.append(line)
          if 'Basis not recognized' in line:
            orcacrash = "yes"
            earlycrash = "yes"
            errormessage.append(line)
          if 'Requested ECP not available' in line:
            orcacrash = "yes"
            earlycrash = "yes"
            errormessage.append(line)
          if 'Element name/number, dummy atom or point charge expected in COORDS' in line:
            coorderror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'FATAL ERROR ENCOUNTERED' in line:
            fatalerrorcode = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'There is no basis function on atom' in line:
            basiserror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'ORCA finished by error termination' in line:
            errortermin = "yes"
            orcacrash = "yes"
            errormessage.append(line)
          if 'An error has occured in the SCF module' in line:
            scferrorgeneral = "yes"
            orcacrash = "yes"
          if 'An error has occured in the CASSCF module' in line:
            casscferrorgeneral = "yes"
            orcacrash = "yes"
            errormessage.append("CASSCF module failed")
          if 'ORCA finished by error termination in CASSCF' in line:
            casscferrorgeneral = "yes"
            orcacrash = "yes"
            errormessage.append("CASSCF module failed")
          if 'mpirun has exited due to process' in line:
            mpiruncode = "yes"
            orcacrash = "yes"
          if 'mpirun noticed that process rank 0' in line:
            mpiruncode2 = "yes"
            orcacrash = "yes"
          if 'Job terminated from outer' in line:
            jobtermin = "yes"
            orcacrash = "yes"
          if 'CANNOT OPEN FILE' in line:
            cannotopenfile = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Error: XYZ File reading requested' in line:
            xyzfileerror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
            errormessage.append("XYZ file error problem")
          if '!!!               Filename:' in line:
            xyzfileerror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
            errormessage.append("XYZ file error problem")
          if 'Unknown identifier in' in line:
            unknownidentifier = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'ERROR: expect a' in line:
            commanderror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'ERROR: found a coordinate defintion' in line:
            coordinateerror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
          if 'Diagonalization failure because of NANs in input matrix' in line:
            diagerror = "yes"
            orcacrash = "yes"
          if 'ERROR       : GSTEP Program returns an error' in line:
            gsteperror = "yes"
            orcacrash = "yes"
          if 'ORCA TERMINATED NORMALLY' in line:
            runcomplete = "yes"
          if 'TOTAL RUN TIME:' in line:
            run_arr = line.split()[3:]
            runtime = float(run_arr[0]) * 86400
            runtime += float(run_arr[2]) * 3600
            runtime += float(run_arr[4]) * 60
            runtime += float(run_arr[6])
            runtime += round(float(run_arr[8]) * 0.001, 0)
          if 'This wavefunction IS NOT CONVERGED!' in line:
            scfconv = "no"
            orcacrash = "yes"
            errormessage.append("SCF did not converge")
          if 'The optimization did not converge but reach' in line:
            optnotconv = "yes"
            print("ddddddddddddddd")
          if 'Error (ORCA_SCFGRAD): cannot find the xc-energy file:' in line:
            scfconv = "no"
            orcacrash = "yes"
            errormessage.append("SCF did not converge")
          if 'Error: XYZ File reading requested but the structur' in line:
            xyzfileerror = "yes"
            orcacrash = "yes"
            earlycrash = "yes"
            errormessage.append("XYZ file error problem")

    data.append([filename, jobtype, method, actualelec, conbf,
                 runtime, parproc])

  # out of loop, create dataframe
  df = pd.DataFrame(
      columns=["path", "jobtype", "method", "nel", "nbas", "time", "cores"],
      data=data)
  df.to_csv("orca_data.csv", index=False)


def getFileList():
  filelist = []
  try:
    for file in glob.glob('./**/*.out', recursive=True):
      if file.endswith(".out"):
        filelist.append(file)

    if len(filelist) == 0:
      print("No files found.", filelist)
      sys.exit()

    return filelist
  except Exception as e:
    print(e)
    sys.exit()


def reverse_lines(filename, BUFSIZE=20480):
  # f = open(filename, "r")
  filename.seek(0, 2)
  p = filename.tell()
  remainder = ""
  while True:
    sz = min(BUFSIZE, p)
    p -= sz
    filename.seek(p)
    buf = filename.read(sz) + remainder
    if '\n' not in buf:
      remainder = buf
    else:
      i = buf.index('\n')
      for L in buf[i+1:].split("\n")[::-1]:
        yield L
      remainder = buf[:i]
    if p == 0:
      break
  yield remainder


def readlastline(file):
  with open(file, "rb") as f:
    first = f.readline()
    last = readlastline(f)

    f.seek(-2, 2)              # Jump to the second last byte.
    while f.read(1) != b"\n":  # Until EOL is found ...
      # ... jump back, over the read byte plus one more.
      f.seek(-2, 1)
    return f.read()            # Read all data from this point on.


if __name__ == '__main__':
  main()
