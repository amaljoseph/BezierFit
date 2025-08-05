import numpy as np
import math

class BezierCurve:
    def __init__(self, degree=2, control_points=None):
        self.degree = degree
        if control_points is None:
            control_points = []
        self.control_points = control_points

    def fit(self, curve_points):
        self.bernstein_polynomials = self.compute_bernstein_polynomials_(num=len(curve_points))
        inv_bernstein_polynomials = np.linalg.pinv(self.bernstein_polynomials)
        self.control_points = inv_bernstein_polynomials @ curve_points
    
    def compute_bernstein_polynomials_(self, num=100, t=None):
        binomial_coefficients = np.array([math.comb(self.degree, i) for i in range(self.degree + 1)]) # Compute Binomial Coefficents

        # Create t values
        if not t: # to compute bernstein coefficents in the range [0, 1]
            T = np.linspace(0, 1, num)
        else: # to compute bernstein coefficents for a particular value of t
            T = t
        T_power = np.array([T**i for i in range(self.degree + 1)])
        one_minus_T_power = np.array([(1 - T)**(self.degree - i) for i in range(self.degree + 1)])
        if t:
            return binomial_coefficients * T_power * one_minus_T_power
        return (binomial_coefficients[:, None] * T_power * one_minus_T_power).T # Compute Bernstein polynomials

    def get_curve(self, num=100):
        assert self.control_points is not None, "Control points cannot be None."
        assert isinstance(self.control_points, (np.ndarray, list)) and all(
            len(point) == 2 for point in self.control_points
        ), "Control points must be a list of (x, y) pairs."
        assert len(self.control_points) == (self.degree + 1), (
            f"Degree mismatch: Expected {self.degree + 1} control points, but got {len(self.control_points)}."
        )
        
        self.bernstein_polynomials = self.compute_bernstein_polynomials_(num=num)
        self.bezier_points = self.bernstein_polynomials @ np.array(self.control_points) # Compute the curve points
        return self.bezier_points
    
    def get_point_at_t(self, t):
        assert 0 <= t <= 1, "t must be between 0 and 1."
        # Compute the Bernstein basis polynomials for the given t
        # binomial_coefficients = np.array([math.comb(self.degree, i) for i in range(self.degree + 1)]) # Compute Binomial Coefficents
        # T_power = np.array([t**i for i in range(self.degree + 1)])
        # one_minus_T_power = np.array([(1 - t)**(self.degree - i) for i in range(self.degree + 1)])

        # bernstein_polynomials_at_t = binomial_coefficients * T_power * one_minus_T_power
        
        bernstein_polynomials_at_t = self.compute_bernstein_polynomials_(t=t)
        # Compute the Bezier point at t by weighting the control points with the Bernstein polynomials
        bezier_point_at_t = np.dot(bernstein_polynomials_at_t, self.control_points)
        
        return bezier_point_at_t

