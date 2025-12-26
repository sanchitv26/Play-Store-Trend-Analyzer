"""
Mock data generator for Play Store reviews
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict

class MockDataGenerator:
    """Generates mock Play Store review data"""
    
    def __init__(self):
        # Common review templates
        self.templates = [
            # Delivery issues
            "Delivery was {time} late. Very disappointed!",
            "Food arrived {condition}. Won't order again.",
            "Delivery partner was {behavior}.",
            "Order tracking not working properly.",
            
            # Food quality issues
            "Food was {quality}. Not worth the price.",
            "Received wrong order. {wrong_item} instead.",
            "Food packaging was damaged.",
            "Some items were missing from my order.",
            
            # App issues
            "App keeps crashing when I try to {action}.",
            "Payment {payment_issue} but money deducted.",
            "Cannot login to my account.",
            "App is very slow and buggy.",
            
            # Positive reviews
            "Great service! Food arrived hot and fresh.",
            "Quick delivery and polite delivery partner.",
            "App works perfectly. Very user friendly.",
            "Excellent customer support.",
            
            # Suggestions
            "Please add {feature}.",
            "Should have {improvement}.",
            "Need better {aspect}.",
        ]
        
        # Fillers for templates
        self.fillers = {
            'time': ['1 hour', '2 hours', '30 minutes', '45 minutes'],
            'condition': ['cold', 'stale', 'spoiled', 'room temperature'],
            'behavior': ['rude', 'impolite', 'unprofessional'],
            'quality': ['poor', 'bad', 'terrible', 'awful'],
            'wrong_item': ['veg burger', 'chicken pizza', 'wrong curry'],
            'action': ['place order', 'make payment', 'track order'],
            'payment_issue': ['failed', 'showed error'],
            'feature': ['dark mode', 'group ordering', 'schedule delivery'],
            'improvement': ['order tracking', 'search function', 'filters'],
            'aspect': ['customer support', 'delivery tracking', 'UI']
        }
    
    def generate_daily_reviews(self, date: datetime, count: int = 50) -> List[Dict]:
        """Generate mock reviews for a specific date"""
        reviews = []
        
        # Vary count by day of week
        day_factor = 1.3 if date.weekday() >= 5 else 1.0
        actual_count = int(count * day_factor * random.uniform(0.8, 1.2))
        
        # Determine if there's a trending issue
        trending_issue = None
        if random.random() < 0.2:
            trending_issue = random.choice(['delivery', 'app', 'food', 'payment'])
        
        for i in range(actual_count):
            # Choose template
            template = random.choice(self.templates)
            
            # Fill template
            content = self._fill_template(template)
            
            # Determine score based on content
            if any(word in content.lower() for word in ['good', 'great', 'excellent', 'perfect']):
                score = random.randint(4, 5)
            elif any(word in content.lower() for word in ['bad', 'poor', 'terrible', 'worst']):
                score = random.randint(1, 2)
            else:
                score = random.randint(3, 4)
            
            # Add trending issue if applicable
            if trending_issue and random.random() < 0.3:
                if trending_issue == 'delivery':
                    content = f"Delivery issues today! {content}"
                elif trending_issue == 'app':
                    content = f"App problems today! {content}"
                elif trending_issue == 'food':
                    content = f"Food quality issues today! {content}"
                else:
                    content = f"Payment issues today! {content}"
            
            review = {
                'content': content,
                'score': score,
                'review_date': date.strftime("%Y-%m-%d"),
                'review_id': f"review_{date.strftime('%Y%m%d')}_{i:04d}",
                'user_name': f"User_{random.randint(1000, 9999)}",
                'thumbs_up_count': random.randint(0, 50)
            }
            
            reviews.append(review)
        
        return reviews
    
    def _fill_template(self, template: str) -> str:
        """Fill template placeholders with random values"""
        result = template
        for key, values in self.fillers.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, random.choice(values))
        return result