// src/core/process/sigmav_interface.cc
#include "sigmav_interface.h"

#include "CPPProcess.h"
#include "momenta.h"

#include <cmath>
#include <stdexcept>
#include <string>

namespace {

// Card path, set once by initProc(), read by each thread's first proc() call.
std::string g_card;

// One CPPProcess per thread. Lazily initialized on first call in that thread.
CPPProcess& proc() {
    thread_local CPPProcess p;
    thread_local bool inited = false;
    if (!inited) {
        if (g_card.empty()) {
            throw std::runtime_error(
                "sigmav_interface::proc(): called before initProc()");
        }
        p.initProc(g_card);
        inited = true;
    }
    return p;
}

} // namespace

namespace sigmav_iface {

void initProc(const std::string& card) {
    g_card = card;
    // Initialize the calling thread's instance now, so errors surface
    // before the caller spawns threads.
    proc();
}

const std::vector<double>& getMasses() {
    return proc().getMasses();
}

const std::vector<std::pair<double, double>>& getNewDOF() {
    return proc().getNewDOF();
}

const std::vector<double>& getNewMasses() {
    return proc().getNewMasses();
}

void setMomenta(std::vector<double*>& ps) {
    proc().setMomenta(ps);
}

double sigmaKin(double s, double theta) {
    // Build momenta for this (s, theta) and feed it to this thread's process.
    std::vector<double*> ps = momenta(2, std::sqrt(s), proc().getMasses(), theta);
    proc().setMomenta(ps);
    return proc().sigmaKin(s, theta);
}

} // namespace sigmav_iface
