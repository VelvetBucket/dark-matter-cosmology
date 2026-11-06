#pragma once
#include <string>
#include <vector>

struct Options {
    std::string inputFile;
    int         N  = 1000;
    double      x0  =  1.e-10;
    double      xf = 1.e+7;
    double      m1 = -1.0;
    bool        neq   = false;
    std::vector<std::string> extras;
};

// Throws std::runtime_error on bad args or --help.
Options parse_args(int argc, char** argv);
