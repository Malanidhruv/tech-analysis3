import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Dict

class CandlestickPatternDetector:
    """
    Comprehensive candlestick pattern detector for technical analysis.
    
    Detects single, two, and three-candlestick patterns using OHLC data.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the pattern detector with OHLC data.
        
        Args:
            df: DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare the data for pattern detection."""
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close']
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Calculate basic candle properties
        self.df['body'] = self.df['close'] - self.df['open']
        self.df['body_size'] = abs(self.df['body'])
        self.df['upper_shadow'] = self.df['high'] - self.df[['open', 'close']].max(axis=1)
        self.df['lower_shadow'] = self.df[['open', 'close']].min(axis=1) - self.df['low']
        self.df['total_size'] = self.df['high'] - self.df['low']
        self.df['is_bullish'] = self.df['body'] > 0
        self.df['is_bearish'] = self.df['body'] < 0
        
        # Calculate average body size for relative measurements
        self.avg_body_size = self.df['body_size'].rolling(window=20, min_periods=1).mean()
        self.avg_total_size = self.df['total_size'].rolling(window=20, min_periods=1).mean()
    
    def detect_all_patterns(self) -> List[str]:
        """
        Detect all candlestick patterns in the data.
        
        Returns:
            List of detected pattern names
        """
        patterns = []
        
        # Single candlestick patterns
        patterns.extend(self._detect_single_candlestick_patterns())
        
        # Two-candlestick patterns
        patterns.extend(self._detect_two_candlestick_patterns())
        
        # Three-candlestick patterns
        patterns.extend(self._detect_three_candlestick_patterns())
        
        return patterns
    
    def _detect_single_candlestick_patterns(self) -> List[str]:
        """Detect single candlestick patterns."""
        patterns = []
        
        if len(self.df) < 1:
            return patterns
        
        current = self.df.iloc[-1]
        avg_body = self.avg_body_size.iloc[-1]
        avg_total = self.avg_total_size.iloc[-1]
        
        # Doji patterns
        if self._is_doji(current, avg_total):
            if self._is_dragonfly_doji(current):
                patterns.append('Dragonfly Doji')
            elif self._is_gravestone_doji(current):
                patterns.append('Gravestone Doji')
            elif (current['upper_shadow'] <= 0.1 * current['total_size'] and 
                  current['lower_shadow'] <= 0.1 * current['total_size']):
                patterns.append('Doji')
            elif self._is_long_legged_doji(current):
                patterns.append('Long-legged Doji')
            else:
                patterns.append('Doji')
        
        # Hammer patterns
        if self._is_hammer(current, avg_body):
            patterns.append('Hammer')
        
        if self._is_inverted_hammer(current, avg_body):
            patterns.append('Inverted Hammer')
        
        if self._is_hanging_man(current, avg_body):
            patterns.append('Hanging Man')
        
        if self._is_shooting_star(current, avg_body):
            patterns.append('Shooting Star')
        
        if self._is_spinning_top(current, avg_body):
            patterns.append('Spinning Top')
        
        # Marubozu patterns
        if self._is_marubozu(current, avg_body):
            if current['is_bullish']:
                patterns.append('Bullish Marubozu')
            else:
                patterns.append('Bearish Marubozu')
        
        return patterns
    
    def _detect_two_candlestick_patterns(self) -> List[str]:
        """Detect two-candlestick patterns."""
        patterns = []
        
        if len(self.df) < 2:
            return patterns
        
        current = self.df.iloc[-1]
        previous = self.df.iloc[-2]
        
        # Engulfing patterns
        if self._is_bullish_engulfing(current, previous):
            patterns.append('Bullish Engulfing')
        
        if self._is_bearish_engulfing(current, previous):
            patterns.append('Bearish Engulfing')
        
        # Harami patterns
        if self._is_bullish_harami(current, previous):
            patterns.append('Bullish Harami')
        
        if self._is_bearish_harami(current, previous):
            patterns.append('Bearish Harami')
        
        if self._is_harami_cross(current, previous):
            patterns.append('Harami Cross')
        
        # Piercing and Dark Cloud Cover
        if self._is_piercing_pattern(current, previous):
            patterns.append('Piercing Pattern')
        
        if self._is_dark_cloud_cover(current, previous):
            patterns.append('Dark Cloud Cover')
        
        # Tweezer patterns
        if self._is_tweezer_tops(current, previous):
            patterns.append('Tweezer Tops')
        
        if self._is_tweezer_bottoms(current, previous):
            patterns.append('Tweezer Bottoms')
        
        return patterns
    
    def _detect_three_candlestick_patterns(self) -> List[str]:
        """Detect three-candlestick patterns."""
        patterns = []
        
        if len(self.df) < 3:
            return patterns
        
        first = self.df.iloc[-3]
        second = self.df.iloc[-2]
        third = self.df.iloc[-1]
        
        # Star patterns
        if self._is_morning_star(first, second, third):
            patterns.append('Morning Star')
        
        if self._is_evening_star(first, second, third):
            patterns.append('Evening Star')
        
        # Three soldiers and crows
        if self._is_three_white_soldiers(first, second, third):
            patterns.append('Three White Soldiers')
        
        if self._is_three_black_crows(first, second, third):
            patterns.append('Three Black Crows')
        
        # Three inside patterns
        if self._is_three_inside_up(first, second, third):
            patterns.append('Three Inside Up')
        
        if self._is_three_inside_down(first, second, third):
            patterns.append('Three Inside Down')
        
        # Three outside patterns
        if self._is_three_outside_up(first, second, third):
            patterns.append('Three Outside Up')
        
        if self._is_three_outside_down(first, second, third):
            patterns.append('Three Outside Down')
        
        return patterns
    
    # Single candlestick pattern detection methods
    def _is_doji(self, candle: pd.Series, avg_total: float) -> bool:
        """Check if candle is a doji."""
        return candle['body_size'] <= 0.1 * candle['total_size']
    
    def _is_dragonfly_doji(self, candle: pd.Series) -> bool:
        """Check if candle is a dragonfly doji."""
        return (candle['body_size'] <= 0.1 * candle['total_size'] and
                candle['upper_shadow'] <= 0.1 * candle['total_size'] and
                candle['lower_shadow'] > 2 * candle['body_size'])
    
    def _is_gravestone_doji(self, candle: pd.Series) -> bool:
        """Check if candle is a gravestone doji."""
        return (candle['body_size'] <= 0.1 * candle['total_size'] and
                candle['lower_shadow'] <= 0.1 * candle['total_size'] and
                candle['upper_shadow'] > 2 * candle['body_size'])
    
    def _is_long_legged_doji(self, candle: pd.Series) -> bool:
        """Check if candle is a long-legged doji."""
        return (candle['body_size'] <= 0.1 * candle['total_size'] and
                candle['upper_shadow'] > 0.2 * candle['total_size'] and
                candle['lower_shadow'] > 0.2 * candle['total_size'])
    
    def _is_hammer(self, candle: pd.Series, avg_body: float) -> bool:
        """Check if candle is a hammer."""
        return (candle['lower_shadow'] > 2 * avg_body and
                candle['upper_shadow'] < avg_body and
                candle['body_size'] < avg_body)
    
    def _is_inverted_hammer(self, candle: pd.Series, avg_body: float) -> bool:
        """Check if candle is an inverted hammer."""
        return (candle['upper_shadow'] > 2 * avg_body and
                candle['lower_shadow'] < avg_body and
                candle['body_size'] < avg_body)
    
    def _is_hanging_man(self, candle: pd.Series, avg_body: float) -> bool:
        """Check if candle is a hanging man."""
        return (candle['lower_shadow'] > 2 * avg_body and
                candle['upper_shadow'] < avg_body and
                candle['body_size'] < avg_body and
                candle['is_bearish'])
    
    def _is_shooting_star(self, candle: pd.Series, avg_body: float) -> bool:
        """Check if candle is a shooting star."""
        return (candle['upper_shadow'] > 2 * avg_body and
                candle['lower_shadow'] < avg_body and
                candle['body_size'] < avg_body and
                candle['is_bearish'])
    
    def _is_spinning_top(self, candle: pd.Series, avg_body: float) -> bool:
        """Check if candle is a spinning top."""
        return (candle['upper_shadow'] > avg_body and
                candle['lower_shadow'] > avg_body and
                candle['body_size'] < avg_body)
    
    def _is_marubozu(self, candle: pd.Series, avg_body: float) -> bool:
        """Check if candle is a marubozu."""
        return (candle['body_size'] > 2 * avg_body and
                candle['upper_shadow'] < 0.1 * candle['body_size'] and
                candle['lower_shadow'] < 0.1 * candle['body_size'])
    
    # Two-candlestick pattern detection methods
    def _is_bullish_engulfing(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is bullish engulfing."""
        return (previous['is_bearish'] and
                current['is_bullish'] and
                current['open'] < previous['close'] and
                current['close'] > previous['open'])
    
    def _is_bearish_engulfing(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is bearish engulfing."""
        return (previous['is_bullish'] and
                current['is_bearish'] and
                current['open'] > previous['close'] and
                current['close'] < previous['open'])
    
    def _is_bullish_harami(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is bullish harami."""
        return (previous['is_bearish'] and
                current['is_bullish'] and
                current['high'] < previous['open'] and
                current['low'] > previous['close'])
    
    def _is_bearish_harami(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is bearish harami."""
        return (previous['is_bullish'] and
                current['is_bearish'] and
                current['high'] < previous['close'] and
                current['low'] > previous['open'])
    
    def _is_harami_cross(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is harami cross."""
        return (self._is_bullish_harami(current, previous) or
                self._is_bearish_harami(current, previous)) and self._is_doji(current, current['total_size'])
    
    def _is_piercing_pattern(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is piercing pattern."""
        return (previous['is_bearish'] and
                current['is_bullish'] and
                current['open'] < previous['low'] and
                current['close'] > previous['close'] + (previous['body_size'] / 2))
    
    def _is_dark_cloud_cover(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is dark cloud cover."""
        return (previous['is_bullish'] and
                current['is_bearish'] and
                current['open'] > previous['high'] and
                current['close'] < previous['close'] - (previous['body_size'] / 2))
    
    def _is_tweezer_tops(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is tweezer tops."""
        return (abs(current['high'] - previous['high']) < 0.1 * current['high'] and
                current['is_bearish'] and previous['is_bullish'])
    
    def _is_tweezer_bottoms(self, current: pd.Series, previous: pd.Series) -> bool:
        """Check if pattern is tweezer bottoms."""
        return (abs(current['low'] - previous['low']) < 0.1 * current['low'] and
                current['is_bullish'] and previous['is_bearish'])
    
    # Three-candlestick pattern detection methods
    def _is_morning_star(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is morning star."""
        return (first['is_bearish'] and
                second['body_size'] < 0.5 * first['body_size'] and
                third['is_bullish'] and
                third['close'] > (first['open'] + first['close']) / 2)
    
    def _is_evening_star(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is evening star."""
        return (first['is_bullish'] and
                second['body_size'] < 0.5 * first['body_size'] and
                third['is_bearish'] and
                third['close'] < (first['open'] + first['close']) / 2)
    
    def _is_three_white_soldiers(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is three white soldiers."""
        return (first['is_bullish'] and second['is_bullish'] and third['is_bullish'] and
                second['open'] > first['open'] and third['open'] > second['open'] and
                second['close'] > first['close'] and third['close'] > second['close'])
    
    def _is_three_black_crows(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is three black crows."""
        return (first['is_bearish'] and second['is_bearish'] and third['is_bearish'] and
                second['open'] < first['open'] and third['open'] < second['open'] and
                second['close'] < first['close'] and third['close'] < second['close'])
    
    def _is_three_inside_up(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is three inside up."""
        return (first['is_bearish'] and
                self._is_bullish_harami(second, first) and
                third['is_bullish'] and third['close'] > second['high'])
    
    def _is_three_inside_down(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is three inside down."""
        return (first['is_bullish'] and
                self._is_bearish_harami(second, first) and
                third['is_bearish'] and third['close'] < second['low'])
    
    def _is_three_outside_up(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is three outside up."""
        return (first['is_bearish'] and
                self._is_bullish_engulfing(second, first) and
                third['is_bullish'] and third['close'] > second['high'])
    
    def _is_three_outside_down(self, first: pd.Series, second: pd.Series, third: pd.Series) -> bool:
        """Check if pattern is three outside down."""
        return (first['is_bullish'] and
                self._is_bearish_engulfing(second, first) and
                third['is_bearish'] and third['close'] < second['low'])


def detect_candlestick_patterns(df: pd.DataFrame) -> List[str]:
    """
    Convenience function to detect candlestick patterns in a DataFrame.
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        List of detected pattern names
    """
    if df.empty or len(df) < 1:
        return []
    
    detector = CandlestickPatternDetector(df)
    return detector.detect_all_patterns()


def get_pattern_description(pattern_name: str) -> str:
    """
    Get description for a candlestick pattern.
    
    Args:
        pattern_name: Name of the pattern
        
    Returns:
        Description of the pattern
    """
    descriptions = {
        # Single candlestick patterns
        'Doji': 'A doji occurs when the open and close prices are virtually equal, indicating indecision in the market.',
        'Hammer': 'A bullish reversal pattern with a small body at the top and a long lower shadow.',
        'Inverted Hammer': 'A bullish reversal pattern with a small body at the bottom and a long upper shadow.',
        'Hanging Man': 'A bearish reversal pattern that looks like a hammer but appears after an uptrend.',
        'Shooting Star': 'A bearish reversal pattern with a small body at the bottom and a long upper shadow.',
        'Spinning Top': 'A pattern indicating indecision with small body and long shadows.',
        'Bullish Marubozu': 'A strong bullish candle with no shadows.',
        'Bearish Marubozu': 'A strong bearish candle with no shadows.',
        'Dragonfly Doji': 'A doji with a long lower shadow and virtually no upper shadow.',
        'Gravestone Doji': 'A doji with a long upper shadow and virtually no lower shadow.',
        'Long-legged Doji': 'A doji with long upper and lower shadows.',
        
        # Two-candlestick patterns
        'Bullish Engulfing': 'A bullish reversal pattern where the current candle completely engulfs the previous bearish candle.',
        'Bearish Engulfing': 'A bearish reversal pattern where the current candle completely engulfs the previous bullish candle.',
        'Bullish Harami': 'A bullish reversal pattern where a small bullish candle is contained within the previous bearish candle.',
        'Bearish Harami': 'A bearish reversal pattern where a small bearish candle is contained within the previous bullish candle.',
        'Harami Cross': 'A harami pattern where the second candle is a doji.',
        'Piercing Pattern': 'A bullish reversal pattern where the current candle opens below the previous low but closes above the midpoint.',
        'Dark Cloud Cover': 'A bearish reversal pattern where the current candle opens above the previous high but closes below the midpoint.',
        'Tweezer Tops': 'Two candles with identical highs, indicating resistance.',
        'Tweezer Bottoms': 'Two candles with identical lows, indicating support.',
        
        # Three-candlestick patterns
        'Morning Star': 'A bullish reversal pattern with a bearish candle, a small-bodied candle, and a bullish candle.',
        'Evening Star': 'A bearish reversal pattern with a bullish candle, a small-bodied candle, and a bearish candle.',
        'Three White Soldiers': 'Three consecutive bullish candles with higher opens and closes.',
        'Three Black Crows': 'Three consecutive bearish candles with lower opens and closes.',
        'Three Inside Up': 'A bullish reversal pattern with a bearish candle, a harami, and a bullish candle.',
        'Three Inside Down': 'A bearish reversal pattern with a bullish candle, a harami, and a bearish candle.',
        'Three Outside Up': 'A bullish reversal pattern with a bearish candle, an engulfing, and a bullish candle.',
        'Three Outside Down': 'A bearish reversal pattern with a bullish candle, an engulfing, and a bearish candle.'
    }
    
    return descriptions.get(pattern_name, 'Pattern description not available.') 