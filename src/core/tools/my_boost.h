#pragma once
#include <functional>

namespace mb {

double gauss_kronrod(const std::function<double(double)>& f,
                     double a, double b,
                     int    max_depth = 15,
                     double rel_tol = 1e-9);

double tanh_sinh(const std::function<double(double)>& f,
                 double a, double b,
                 double rel_tol = 1e-9);

} // namespace mb
