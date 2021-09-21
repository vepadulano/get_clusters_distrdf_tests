from time import time

import ROOT

filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)
             ]

if __name__ == "__main__":
    ROOT.gSystem.CompileMacro("compiled_threadexecutor.cpp","O")

    from ROOT import openfiles_MT

    with open("benchmarks/open_root_files_threadexecutor_compiled.csv", "a+") as f:
        for _ in range(10):
            print("Opening remote files...")
            start = time()
            files = openfiles_MT(filenames)
            end = time()

            f.write("{}\n".format(round(end - start, 2)))
