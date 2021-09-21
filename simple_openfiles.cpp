#include <TFile.h>
#include <string>
#include <array>

int main() {
    std::array<TFile *, 100> files;
    for (auto i = 1u; i < 101; i++) {
        const std::string filename = "root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"
                                     + std::to_string(i) + ".root";
        files[i-1] = TFile::Open(filename.c_str());
    }
}