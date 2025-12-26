"""
Review analyzer for extracting topics from reviews
"""
import re
from typing import List, Dict

class ReviewAnalyzer:
    """Analyzes reviews to extract topics"""
    
    def __init__(self):
        # Topic keywords mapping
        self.topic_patterns = {
            'Delivery issue': [
                r'delivery.*late', r'delivery.*delay', r'late.*delivery',
                r'delayed', r'not.*delivered', r'missed.*delivery'
            ],
            'Food stale': [
                r'food.*cold', r'cold.*food', r'stale', 
                r'not.*fresh', r'spoiled', r'bad.*food'
            ],
            'Delivery partner rude': [
                r'rude', r'impolite', r'bad.*behavior',
                r'unprofessional', r'argu.*', r'disrespect'
            ],
            'App crashing': [
                r'app.*crash', r'crash.*app', r'freeze',
                r'not.*respond', r'hangs', r'bug.*app'
            ],
            'Payment issue': [
                r'payment.*fail', r'fail.*payment', r'transaction.*fail',
                r'money.*deducted', r'refund', r'payment.*problem'
            ],
            'Order cancellation': [
                r'order.*cancel', r'cancel.*order', r'cancelled',
                r'order.*not.*placed', r'auto.*cancel'
            ],
            'Food quality poor': [
                r'quality.*poor', r'bad.*quality', r'taste.*bad',
                r'not.*good', r'worst.*food', r'tasteless'
            ],
            'Wrong order delivered': [
                r'wrong.*order', r'incorrect.*order', r'not.*what.*ordered',
                r'mistake.*order', r'wrong.*item'
            ],
            'Long delivery time': [
                r'long.*time', r'takes.*hours', r'slow.*delivery',
                r'waiting.*long', r'delivery.*slow'
            ],
            'Customer support unresponsive': [
                r'support', r'customer.*service', r'no.*response',
                r'help', r'contact', r'assistance'
            ],
        }
    
    def extract_topics(self, reviews: List[Dict]) -> Dict[str, List[str]]:
        """Extract topics from a batch of reviews"""
        daily_topics = {}
        
        for review in reviews:
            content = review.get('content', '').lower()
            
            # Check each topic pattern
            for topic, patterns in self.topic_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        if topic not in daily_topics:
                            daily_topics[topic] = []
                        daily_topics[topic].append(review['content'])
                        break  # Stop checking other patterns for this topic
        
        return daily_topics
    
    def count_topics(self, topics_dict: Dict[str, List[str]]) -> Dict[str, int]:
        """Count occurrences of each topic"""
        counts = {}
        for topic, reviews in topics_dict.items():
            counts[topic] = len(reviews)
        return counts