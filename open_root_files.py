from time import time

import ROOT

def open_files(filenames):
    return [ROOT.TFile.Open(filename) for filename in filenames]

filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)
             ]

if __name__ == "__main__":

    with open("benchmarks/open_root_files.csv", "a+") as f:
        for _ in range(5):
            print("Opening remote files...")
            start = time()
            files = open_files(filenames)
            end = time()

            f.write("{}\n".format(round(end - start, 2)))
