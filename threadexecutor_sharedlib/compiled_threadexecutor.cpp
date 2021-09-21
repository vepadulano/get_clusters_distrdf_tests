#include "compiled_threadexecutor.hxx"

void openfiles_MT(const std::vector<std::string> &filenames) {
  ROOT::TThreadExecutor executor;
  executor.Foreach(
      [](const std::string &filename) { return TFile::Open(filename.c_str()); },
      filenames);
}