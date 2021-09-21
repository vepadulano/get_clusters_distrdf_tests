#include "compiled_sequential.hxx"

void openfiles_sequential(const std::vector<std::string> &filenames) {
  for (const auto &filename: filenames){
    TFile::Open(filename.c_str());
  }
}