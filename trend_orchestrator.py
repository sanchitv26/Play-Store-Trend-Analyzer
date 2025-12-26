"""
Trend analysis orchestrator - main processing engine
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import Config
from review_analyzer import ReviewAnalyzer

class TrendAnalysisOrchestrator:
    """Orchestrates the trend analysis pipeline"""
    
    def __init__(self):
        self.daily_counts = {}
        self.review_analyzer = ReviewAnalyzer()
    
    def process_daily_batch(self, reviews: List[Dict], date: datetime) -> Dict:
        """Process a daily batch of reviews"""
        try:
            date_str = date.strftime("%Y-%m-%d")
            
            # Extract topics from reviews
            topics_dict = self.review_analyzer.extract_topics(reviews)
            
            # Count topics
            topic_counts = self.review_analyzer.count_topics(topics_dict)
            
            # Store counts
            self.daily_counts[date_str] = topic_counts
            
            return {
                'date': date_str,
                'review_count': len(reviews),
                'topic_count': len(topics_dict),
                'unique_topics': list(topic_counts.keys()),
                'topics_dict': topics_dict
            }
            
        except Exception as e:
            print(f"Error processing batch for {date}: {e}")
            return {'date': date.strftime("%Y-%m-%d"), 'error': str(e)}
    
    def generate_trend_report(self, target_date: datetime) -> pd.DataFrame:
        """Generate trend report for the lookback period"""
        if not self.daily_counts:
            print("No data available. Generating sample report...")
            return self._generate_sample_report(target_date)
        
        # Get date range
        dates = []
        for i in range(Config.LOOKBACK_DAYS, -1, -1):
            date = target_date - timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
        
        # Get all unique topics across all days
        all_topics = set()
        for day_counts in self.daily_counts.values():
            all_topics.update(day_counts.keys())
        all_topics = sorted(all_topics)
        
        # Create DataFrame
        data = {}
        for topic in all_topics:
            frequencies = []
            for date_str in dates:
                count = self.daily_counts.get(date_str, {}).get(topic, 0)
                frequencies.append(count)
            data[topic] = frequencies
        
        # Create and return DataFrame
        df = pd.DataFrame(data, index=dates).T
        
        # Filter out topics with very low frequency
        total_mentions = df.sum(axis=1)
        df = df[total_mentions >= Config.MIN_TOPIC_FREQUENCY]
        
        return df
    
    def _generate_sample_report(self, target_date: datetime) -> pd.DataFrame:
        """Generate sample report for demonstration"""
        # Generate date range
        dates = []
        for i in range(Config.LOOKBACK_DAYS, -1, -1):
            date = target_date - timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
        
        # Generate sample data
        np.random.seed(42)
        
        # Use a subset of seed topics
        topics = Config.SEED_TOPICS[:15]
        data = {}
        
        for i, topic in enumerate(topics):
            # Create different trend patterns
            if i % 3 == 0:  # Increasing trend
                base = np.random.randint(1, 5)
                trend = np.linspace(base, base + 20, len(dates))
                noise = np.random.normal(0, 3, len(dates))
            elif i % 3 == 1:  # Decreasing trend
                base = np.random.randint(15, 25)
                trend = np.linspace(base, max(1, base - 15), len(dates))
                noise = np.random.normal(0, 3, len(dates))
            else:  # Random trend
                base = np.random.randint(5, 15)
                trend = np.full(len(dates), base)
                # Add some spikes
                spike_days = np.random.choice(len(dates), size=3, replace=False)
                trend[spike_days] += np.random.randint(5, 15, 3)
                noise = np.random.normal(0, 2, len(dates))
            
            frequencies = np.round(np.maximum(trend + noise, 0)).astype(int)
            data[topic] = frequencies
        
        return pd.DataFrame(data, index=dates).T