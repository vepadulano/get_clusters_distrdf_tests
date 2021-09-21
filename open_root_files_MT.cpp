#include <fstream>
#include <iomanip> // std::setprecision
#include <iostream>
#include <string>

#include <TFile.h>
#include <TStopwatch.h>
#include <ROOT/TThreadExecutor.hxx>
#include <TROOT.h>

static std::string filenametemplate{"root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"};

void openfile(int index){
    std::string filename{filenametemplate + std::to_string(index) + ".root"};
    TFile::Open(filename.c_str());
}

int main()
{

    std::vector<int> indexes(100);
    std::iota(indexes.begin(), indexes.end(), 1);

    std::string outcsv{"benchmarks/open_root_files_cpp_MT.csv"};
    std::ofstream timecsv{outcsv.c_str(), std::ofstream::out | std::ofstream::app};

    for(int i = 0; i < 10; i++){
        ROOT::TThreadExecutor executor;
        TStopwatch watch;
        executor.Foreach(openfile, indexes);
        double elapsed{watch.RealTime()};

        // Store elapsed time in a csv file
        std::cout << "Files opened in: " << std::fixed << std::setprecision(2) << elapsed << " s\n";

        timecsv << std::fixed << std::setprecision(2) << elapsed << "\n";
    }
    timecsv.close();
}
