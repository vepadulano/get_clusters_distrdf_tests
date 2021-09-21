Tests to explore ways to improve on sequential reading of multiple remote `ROOT.TFile` objects for further processing.

Tests are written to output their runtime in csv files in the `benchmarks` folder.

Baseline tests:

* `open_root_files[.py,.cpp]`: sequential read of 100 files from EOS. File pointers are returned in a list to the caller
* `sequential_sharedlib`: folder containing the same test as above but using a shared library to define the function that will read the remote files.

Minimal tests: the `simple_*` tests are the most minimal examples of the functions. Useful for profiling.



