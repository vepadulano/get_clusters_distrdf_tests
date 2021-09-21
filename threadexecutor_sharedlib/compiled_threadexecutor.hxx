#include <string>
#include <vector>

#include <ROOT/TThreadExecutor.hxx>
#include <TFile.h>

void openfiles_MT(const std::vector<std::string> &filenames);
