#include <fstream>
#include <iomanip> // std::setprecision
#include <iostream>
#include <string>

#include <TFile.h>
#include <TStopwatch.h>


#include "compiled_sequential.hxx"

int main()
{
    static std::string filenametemplate{"root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"};
    static std::string outcsv{"../benchmarks/openfiles_sequential_sharedlib.csv"};

    std::vector<std::string> filenames;
    filenames.reserve(100);
    for (int i = 1; i < 101; i ++){
        filenames.emplace_back(filenametemplate + std::to_string(i) + ".root");
    }

    std::ofstream timecsv{outcsv.c_str(), std::ofstream::out | std::ofstream::app};
    for (int i = 0; i < 5; i++){
        TStopwatch watch;
        openfiles_sequential(filenames);
        double elapsed{watch.RealTime()};

        // Store elapsed time in a csv file
        std::cout << "Files opened in: " << std::fixed << std::setprecision(2) << elapsed << " s\n";

        timecsv << std::fixed << std::setprecision(2) << elapsed << "\n";
    }
    timecsv.close();


}
