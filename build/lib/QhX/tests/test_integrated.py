import unittest
from QhX.utils.mock_lc import simple_mock_lc
from QhX.algorithms.wavelets.wwtz import hybrid2d  # Only import what you need
from QhX.calculation import periods, signif_johnson

class TestIntegratedLightCurveProcessing(unittest.TestCase):
    """
    Test suite for integrated light curve processing using wavelet
    transformation and period detection functions.
    """

    def test_light_curve_processing(self):
        """
        Tests the generation and processing of a mock light curve, including
        wavelet matrix coefficient calculations and period/significance calculation.
        """
        print("Running integrated test on single light curve simulation.")

        # Generate mock light curve data
        period = 100  # days
        amplitude = 0.3
        tt, yy = simple_mock_lc(time_interval=10, num_points=1000, frequency=period, amplitude=amplitude, percent=0.5, magnitude=22)

        # Process with hybrid2d
        wwz_matrix, corr, _ = hybrid2d(tt, yy, 80, 800, minfq=2000, maxfq=10)

        # Define example parameters for testing
        numlc = 10  # Number of light curves for Johnson method
        peak = 0  # Example peak position
        idx_peaks = [0]  # Example index of peak, assuming a single peak

        # Detect periods in the correlation matrix
        _, _, r_periods0, up0, low0 = periods(numlc, corr, 800, plot=False, minfq=2000, maxfq=10)

        # Calculate significance
        _, _, sig, _ = signif_johnson(numlc, peak, idx_peaks, [], tt, yy, ntau=80, ngrid=800, f=2, peakHeight=0.6, minfq=2000, maxfq=10)

        # Assertions to verify integration of functions
        self.assertEqual(len(tt), len(yy), "Time and signal arrays should be the same length")
        self.assertIsNotNone(wwz_matrix, "Wavelet matrix calculation failed")
        self.assertIsNotNone(r_periods0, "Period detection failed")
        self.assertGreaterEqual(sig, 0, "Significance should be non-negative")

        # Print results for visual verification
        print('Simulated period (days):', period)
        print('Detected periods (days):', r_periods0)
        print('Upper and lower error bounds (days):', up0, low0)
        print('Significance of detected period:', sig)

if __name__ == '__main__':
    unittest.main()
