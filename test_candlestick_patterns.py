import pandas as pd
import numpy as np
import unittest
from candlestick_patterns import CandlestickPatternDetector, detect_candlestick_patterns, get_pattern_description

class TestCandlestickPatterns(unittest.TestCase):
    """Test cases for candlestick pattern detection."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample OHLC data
        self.sample_data = pd.DataFrame({
            'open': [100, 105, 110, 108, 112, 115, 113, 118, 120, 122],
            'high': [107, 112, 115, 113, 118, 120, 117, 125, 128, 130],
            'low': [98, 103, 108, 105, 110, 112, 110, 115, 118, 120],
            'close': [105, 110, 108, 112, 115, 113, 118, 120, 122, 125],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
    
    def test_doji_detection(self):
        """Test doji pattern detection."""
        # Create a doji candle - open and close should be very close, small shadows
        doji_data = pd.DataFrame({
            'open': [100.0, 105.0, 110.0, 108.0, 112.0, 115.0, 113.0, 118.0, 120.0, 100.0],
            'high': [107.0, 112.0, 115.0, 113.0, 118.0, 120.0, 117.0, 125.0, 128.0, 100.05],
            'low': [98.0, 103.0, 108.0, 105.0, 110.0, 112.0, 110.0, 115.0, 118.0, 99.95],
            'close': [105.0, 110.0, 108.0, 112.0, 115.0, 113.0, 118.0, 120.0, 122.0, 100.0],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        
        patterns = detect_candlestick_patterns(doji_data)
        # Accept either Doji or Long-legged Doji as both are valid doji patterns
        self.assertTrue(any('Doji' in pattern for pattern in patterns))
    
    def test_hammer_detection(self):
        """Test hammer pattern detection."""
        # Create a hammer candle
        hammer_data = pd.DataFrame({
            'open': [100, 105, 110, 108, 112, 115, 113, 118, 120, 100],
            'high': [107, 112, 115, 113, 118, 120, 117, 125, 128, 102],
            'low': [98, 103, 108, 105, 110, 112, 110, 115, 118, 90],
            'close': [105, 110, 108, 112, 115, 113, 118, 120, 122, 101],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        
        patterns = detect_candlestick_patterns(hammer_data)
        self.assertIn('Hammer', patterns)
    
    def test_bullish_engulfing_detection(self):
        """Test bullish engulfing pattern detection."""
        # Create bullish engulfing pattern - previous bearish, current bullish and engulfs
        engulfing_data = pd.DataFrame({
            'open': [100, 105, 110, 108, 112, 115, 113, 118, 120, 95],
            'high': [107, 112, 115, 113, 118, 120, 117, 125, 128, 125],
            'low': [98, 103, 108, 105, 110, 112, 110, 115, 118, 94],
            'close': [105, 110, 108, 112, 115, 113, 118, 120, 122, 124],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        
        # Ensure previous candle is bearish and current is bullish
        engulfing_data.loc[8, 'close'] = 115  # Make previous bearish
        engulfing_data.loc[8, 'open'] = 120   # Previous open higher than close
        engulfing_data.loc[9, 'open'] = 95    # Current open below previous close
        engulfing_data.loc[9, 'close'] = 124  # Current close above previous open
        
        patterns = detect_candlestick_patterns(engulfing_data)
        self.assertIn('Bullish Engulfing', patterns)
    
    def test_morning_star_detection(self):
        """Test morning star pattern detection."""
        # Create morning star pattern - bearish, small body, bullish
        morning_star_data = pd.DataFrame({
            'open': [100, 105, 110, 108, 112, 115, 113, 118, 120, 95],
            'high': [107, 112, 115, 113, 118, 120, 117, 125, 128, 105],
            'low': [98, 103, 108, 105, 110, 112, 110, 115, 118, 94],
            'close': [105, 110, 108, 112, 115, 113, 118, 120, 122, 104],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        
        # Create proper morning star pattern
        morning_star_data.loc[7, 'open'] = 120.0  # First candle bearish
        morning_star_data.loc[7, 'close'] = 118.0 # First candle bearish
        morning_star_data.loc[8, 'open'] = 115.0  # Second candle small body
        morning_star_data.loc[8, 'close'] = 115.1 # Second candle small body
        morning_star_data.loc[9, 'open'] = 110.0  # Third candle bullish
        morning_star_data.loc[9, 'close'] = 125.0 # Third candle bullish
        
        patterns = detect_candlestick_patterns(morning_star_data)
        self.assertIn('Morning Star', patterns)
    
    def test_three_white_soldiers_detection(self):
        """Test three white soldiers pattern detection."""
        # Create three white soldiers pattern
        soldiers_data = pd.DataFrame({
            'open': [100, 105, 110, 108, 112, 115, 113, 118, 120, 122],
            'high': [107, 112, 115, 113, 118, 120, 117, 125, 128, 130],
            'low': [98, 103, 108, 105, 110, 112, 110, 115, 118, 120],
            'close': [105, 110, 108, 112, 115, 113, 118, 120, 122, 125],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
        
        patterns = detect_candlestick_patterns(soldiers_data)
        self.assertIn('Three White Soldiers', patterns)
    
    def test_pattern_descriptions(self):
        """Test pattern description function."""
        description = get_pattern_description('Doji')
        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0)
        
        description = get_pattern_description('Hammer')
        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0)
    
    def test_empty_dataframe(self):
        """Test pattern detection with empty DataFrame."""
        empty_df = pd.DataFrame()
        patterns = detect_candlestick_patterns(empty_df)
        self.assertEqual(patterns, [])
    
    def test_single_row_dataframe(self):
        """Test pattern detection with single row DataFrame."""
        single_row_df = pd.DataFrame({
            'open': [100],
            'high': [105],
            'low': [98],
            'close': [102],
            'volume': [1000]
        })
        patterns = detect_candlestick_patterns(single_row_df)
        # Should only detect single candlestick patterns
        self.assertIsInstance(patterns, list)
    
    def test_all_pattern_types(self):
        """Test that all pattern types are detected."""
        detector = CandlestickPatternDetector(self.sample_data)
        patterns = detector.detect_all_patterns()
        
        # Check that patterns are returned as a list
        self.assertIsInstance(patterns, list)
        
        # Check that all pattern names are strings
        for pattern in patterns:
            self.assertIsInstance(pattern, str)
    
    def test_detector_initialization(self):
        """Test CandlestickPatternDetector initialization."""
        detector = CandlestickPatternDetector(self.sample_data)
        
        # Check that required columns are added
        required_cols = ['body', 'body_size', 'upper_shadow', 'lower_shadow', 
                        'total_size', 'is_bullish', 'is_bearish']
        for col in required_cols:
            self.assertIn(col, detector.df.columns)
    
    def test_invalid_dataframe(self):
        """Test pattern detection with invalid DataFrame."""
        invalid_df = pd.DataFrame({'open': [100]})  # Missing required columns
        
        with self.assertRaises(ValueError):
            CandlestickPatternDetector(invalid_df)

def run_performance_test():
    """Run performance test with large dataset."""
    print("Running performance test...")
    
    # Create large dataset
    n_rows = 10000
    large_df = pd.DataFrame({
        'open': np.random.uniform(100, 200, n_rows),
        'high': np.random.uniform(110, 220, n_rows),
        'low': np.random.uniform(90, 180, n_rows),
        'close': np.random.uniform(100, 200, n_rows),
        'volume': np.random.uniform(1000, 10000, n_rows)
    })
    
    import time
    start_time = time.time()
    patterns = detect_candlestick_patterns(large_df)
    end_time = time.time()
    
    print(f"Processed {n_rows} rows in {end_time - start_time:.2f} seconds")
    print(f"Detected {len(patterns)} patterns")
    
    return end_time - start_time

if __name__ == '__main__':
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test() 