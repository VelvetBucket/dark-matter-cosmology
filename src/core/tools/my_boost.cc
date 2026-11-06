#include "my_boost.h"    

#include <boost/math/quadrature/gauss_kronrod.hpp>
#include <boost/math/quadrature/tanh_sinh.hpp>

#include <cmath>
#include <stdexcept>
#include <string>

namespace mb {

double gauss_kronrod(const std::function<double(double)>& f,
                     double a, double b,
                     int    max_depth,
                     double rel_tol)
{
    namespace bq = boost::math::quadrature;
    double error = 0.0;
    double result = bq::gauss_kronrod<double, 15>::integrate(
        f, a, b,
        static_cast<unsigned>(max_depth),   // gauss_kronrod has max_depth
        rel_tol,                            // tolerance
        &error);

    if (!std::isfinite(result))
        throw std::runtime_error("mb::gauss_kronrod: non-finite result");
    return result;
}

double tanh_sinh(const std::function<double(double)>& f,
                 double a, double b,
                 double rel_tol)
{
    namespace bq = boost::math::quadrature;

    bq::tanh_sinh<double> integrator;         // ← the object

    double error  = 0.0;
    double result = integrator.integrate(
        f, a, b,
        rel_tol,        // tolerance — tanh_sinh has NO max_depth
        &error);

    if (!std::isfinite(result))
        throw std::runtime_error("mb::tanh_sinh: non-finite result");
    return result;
}
} // namespace mb
