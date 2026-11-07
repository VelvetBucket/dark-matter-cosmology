#include "options.h"

#include <boost/program_options.hpp>
#include <stdexcept>
#include <iostream>

using namespace std;
namespace po = boost::program_options;

Options parse_args(int argc, char** argv) {
    Options opt;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "Help screen")
        ("neq", "Generate x vs n_equilibrium table")
        ("input-card", po::value<string>()->required(), "Param card to analyze")
        ("x0", po::value<double>(&opt.x0)->default_value(1.e-7), "Initial value for x")
        ("xf", po::value<double>(&opt.xf)->default_value(1.e+7), "Final value for x")
        ("mDM,m", po::value<double>(&opt.m1), "Mass of the dark matter candidate in GeV")
        ("n-points,n", po::value<int>(&opt.N)->default_value(1000), "Number of points between x0 and xf (inclusive) to be evaluated");

    po::variables_map vm;
    try {
        po::store(po::parse_command_line(argc, argv, desc), vm);

        if (vm.count("help")) {
            std::cout << desc << "\n";
            throw std::runtime_error("help requested");
        }

        po::notify(vm);
    }
    catch (const po::error& e) {
        throw std::runtime_error(std::string("command line error: ") + e.what());
    }
    
    if (vm.count("neq")) opt.neq = true;
    opt.inputFile = vm["input-card"].as<std::string>();
    return opt;
}
