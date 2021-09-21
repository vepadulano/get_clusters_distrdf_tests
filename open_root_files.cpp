#include <fstream>
#include <iomanip> // std::setprecision
#include <iostream>
#include <string>

#include <TFile.h>
#include <TStopwatch.h>

int main()
{
    static std::string filenametemplate{"root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"};
    static std::string outcsv{"benchmarks/open_root_files_cpp.csv"};
    std::ofstream timecsv{outcsv.c_str(), std::ofstream::out | std::ofstream::app};

    for(int j = 0; j < 10; j++){
        TStopwatch watch;
        for (int i = 1; i < 101; i++)
        {
            std::string filename{filenametemplate + std::to_string(i) + ".root"};
            TFile::Open(filename.c_str());
        }
        double elapsed{watch.RealTime()};

        // Store elapsed time in a csv file
        std::cout << "Files opened in: " << std::fixed << std::setprecision(2) << elapsed << " s\n";

        timecsv << std::fixed << std::setprecision(2) << elapsed << "\n";
    }
    timecsv.close();
}
