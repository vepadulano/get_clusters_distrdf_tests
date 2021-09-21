#include <TFile.h>
#include <string>
#include <chrono>
#include <thread>
#include <array>

auto asyncopen(const std::string &filename) {
  auto handle = TFile::AsyncOpen(filename.c_str());
  while (TFile::GetAsyncOpenStatus(handle) != TFile::kAOSSuccess) {
    using namespace std::chrono_literals;
    std::this_thread::sleep_for(0.1s);
  }

  return handle;
}

int main() {
  std::array<TFileOpenHandle *, 100> handles;
  for (auto i = 1u; i < 101; i++) {
    const std::string filename =
        "root://eospublic.cern.ch//eos/root-eos/benchmark/CMSOpenDataDimuon/"
        "Run2012BC_DoubleMuParked_Muons_" +
        std::to_string(i) + ".root";
    handles[i-1] = asyncopen(filename);
  }
}