#include <iostream>
#include <string>
#include <vector>

#include <ROOT/TThreadExecutor.hxx>
#include <TFile.h>

// std::vector<TFile *> openfiles_MT(const std::vector<std::string> &filenames)
// {
//   ROOT::TThreadExecutor executor;
//   return executor.Map(
//       [](const std::string &filename) { return TFile::Open(filename.c_str());
//       }, filenames);
// }

void openfiles_sequential(const std::vector<std::string> &filenames) {
  for (const auto &filename: filenames){
    TFile::Open(filename.c_str());
  }
}

// void openfiles_MT() {
//   static std::string
//   filenametemplate{"root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/Run2012BC_DoubleMuParked_Muons_"};
//   std::vector<int> indexes(100);;
//   std::iota(indexes.begin(), indexes.end(), 1);

//   ROOT::TThreadExecutor executor;
//   executor.Foreach(
//       [](int index) { std::string filename{filenametemplate +
//       std::to_string(index) + ".root"}; TFile::Open(filename.c_str()); },
//       indexes);
// }