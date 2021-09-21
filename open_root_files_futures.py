import concurrent.futures

from time import time

import ROOT

def open_file(filename):
    return ROOT.TFile.Open(filename)


def open_files(filenames):

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

        futures = [executor.submit(open_file, filename) for filename in filenames]
        concurrent.futures.wait(futures)

    return [future.result() for future in futures]


filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)
             ]

if __name__ == "__main__":
    ROOT.EnableThreadSafety()

    with open("benchmarks/open_root_files_futures.csv", "a+") as f:
        for _ in range(5):
            print("Opening remote files...")
            start = time()
            files = open_files(filenames)
            end = time()

            f.write("{}\n".format(round(end - start, 2)))
