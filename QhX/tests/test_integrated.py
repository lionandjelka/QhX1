import unittest
from QhX.utils.mock_lc import simple_mock_lc
from QhX.utils import  correlation
from QhX.algorithms.wavelets.wwtz import *  
#from QhX.algorithms.wavelets.wwt import hybrid2d, inp_param,estimate_wavelet_periods
from QhX.calculation import periods, signif_johnson  
from QhX.plots.reg import plt_freq_heatmap, fig_plot


class TestIntegratedLightCurveProcessing(unittest.TestCase):

    def test_light_curve_processing(self):
        # Generate mock light curve
        print("Running integrated  test on simulation of single light curve, and functionalities of modules")
        print(" for Wavelet matrix coefficients calculations and period and its significance calculation. This may take time about 500-800 seconds...")
        
        period = 100  # days
        amplitude = 0.3
        tt, yy = simple_mock_lc(time_interval=10, num_points=1000, frequency=period, amplitude=amplitude, percent=0.5, magnitude=22)
        #fig_plot(tt, yy)
        # Process with hybrid2d
      
        wwz_matrix, corr, extent = hybrid2d(tt, yy, 80, 800, minfq=2000,maxfq=10)
      
        
        # Assuming the use of a function like signif_johnson (though not explicitly found in the provided notebook cells)
        numlc1 =10  # Example Object ID
        numlc=10 #number of lc for johnson method
        peak = 0  # Example peak position
        idx_peaks = [0]  # Example index of peak, assuming a single peak
        # Extract periods
        # Detect periods in the correlation matrix and store results in peaks0, hh0, r_periods0, up0, low0
        peaks0, hh0, r_periods0, up0, low0 = periods(numlc1, corr, 800, plot=False, minfq=2000, maxfq=10)
    
        yax = corr.flatten()  # Example correlation of oscillation patterns
        bins, bins11, sig, siger = signif_johnson(numlc,peak, idx_peaks, hh0, tt, yy, ntau=80, ngrid=800, f=2, peakHeight=0.6, minfq=2000, maxfq=10)

        # Assertions to verify the integration of functions
        self.assertTrue(len(tt) == len(yy))
        self.assertIsNotNone(wwz_matrix)
        self.assertIsNotNone(r_periods0)
        print('results of individual testings of modules for period detection and significance')
        print('simulated period in days', period)
        print('list of periods in days',r_periods0)
        print ('upper and lower errors in days', up0, low0)
        # Uncomment and modify the following line based on actual implementation of signif_johnson
        self.assertIsNotNone(sig, 0)  # Example condition, should be between 0 and 1
        print('number of simulated shuffled light curves', numlc)
        print('experimental significance', sig)
if __name__ == '__main__':
    unittest.main()
