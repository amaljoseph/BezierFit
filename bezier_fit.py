import numpy as np
import math

class BezierCurve:
    def __init__(self, degree=2, control_points=None):
        self.degree = degree
        if control_points is None:
            control_points = []
        self.control_points = control_points

    def fit(self, curve_points):
        bernstein_polynomials = self.compute_bernstein_polynomials(num=len(curve_points))
        inv_bernstein_polynomials = np.linalg.pinv(bernstein_polynomials)
        self.control_points = inv_bernstein_polynomials @ curve_points
    
    def compute_bernstein_polynomials(self, num=100):
        binomial_coefficients = np.array([math.comb(self.degree, i) for i in range(self.degree + 1)]) # Compute Binomial Coefficents

        # Create t values
        T = np.linspace(0, 1, num)
        T_power = np.array([T**i for i in range(self.degree + 1)])
        one_minus_T_power = np.array([(1 - T)**(self.degree - i) for i in range(self.degree + 1)])
        
        return (binomial_coefficients[:, None] * T_power * one_minus_T_power).T # Compute Bernstein polynomials

    def get_curve(self, num=100):
        assert self.control_points is not None, "Control points cannot be None."
        assert isinstance(self.control_points, (np.ndarray, list)) and all(
            len(point) == 2 for point in self.control_points
        ), "Control points must be a list of (x, y) pairs."
        assert len(self.control_points) == (self.degree + 1), (
            f"Degree mismatch: Expected {self.degree + 1} control points, but got {len(self.control_points)}."
        )
        self.bernstein_polynomials = self.compute_bernstein_polynomials(num=num)
        self.bezier_points = self.bernstein_polynomials @ np.array(self.control_points) # Compute the curve points
        return self.bezier_points

