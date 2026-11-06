// src/core/process/sigmav_interface.h
#pragma once

#include <string>
#include <utility>
#include <vector>

namespace sigmav_iface {

void initProc(const std::string& card);

const std::vector<double>& getMasses();
const std::vector<std::pair<double, double>>& getNewDOF();
const std::vector<double>& getNewMasses();

void setMomenta(std::vector<double*>& ps);
double sigmaKin(double s, double theta);

} // namespace sigmav_iface
