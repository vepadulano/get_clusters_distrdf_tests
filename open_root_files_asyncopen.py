import concurrent.futures

import time

import ROOT

def asyncopen(filename, timeout=20):
    handle = ROOT.TFile.AsyncOpen(filename)

    while timeout > 0 and ROOT.TFile.GetAsyncOpenStatus(handle) == ROOT.TFile.kAOSInProgress: # kAOSInProgress
        time.sleep(0.1)
        timeout -= 0.1

    if timeout == 0:
        return None
    else:
        return handle


def open_files(filenames):

    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = [executor.submit(asyncopen, filename) for filename in filenames]
        concurrent.futures.wait(futures)

    return [ROOT.TFile.Open(future.result()) for future in futures]

treenames = ["Events"] * 100
filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)
             ]

if __name__ == "__main__":

    with open("benchmarks/open_root_files_asyncopen.csv", "a+") as f:
        for _ in range(5):
            print("Opening remote files...")
            start = time.time()
            files = open_files(filenames)
            end = time.time()

            f.write("{}\n".format(round(end - start, 2)))
