import concurrent.futures

from time import time

import ROOT

treenames = ["Events"] * 100
filetemplate = "root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"
filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)
             ]
indexes = [index for index in range(1,101)]
ROOT.gInterpreter.Declare("""
static std::string filetemplate{"root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"};

TFile *open_file(int index){
    std::string filename{filetemplate + std::to_string(index) + ".root"};
    return TFile::Open(filename.c_str());
};

struct fileopener{

    TFile *operator()(int index){
        std::string filename{filetemplate + std::to_string(index) + ".root"};
        return TFile::Open(filename.c_str());
    }

};
""")

if __name__ == "__main__":

    with open("benchmarks/open_root_files_threadexecutor.csv", "a+") as f:
        for _ in range(5):
            print("Opening remote files...")
            executor = ROOT.TThreadExecutor()
            start = time()
            executor.Foreach(ROOT.fileopener(), indexes)
            end = time()

            f.write("{}\n".format(round(end - start, 2)))
