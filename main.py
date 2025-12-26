"""
Main entry point for Play Store Trend Analyzer
"""
import asyncio
import argparse
import sys
from datetime import datetime, timedelta

from config import Config
from mock_data import MockDataGenerator
from trend_orchestrator import TrendAnalysisOrchestrator
from utils import print_report_summary, save_reports

def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD")
        sys.exit(1)

async def main():
    """Main function to run the trend analyzer"""
    parser = argparse.ArgumentParser(
        description="Play Store Trend Analyzer - Analyze app review trends"
    )
    parser.add_argument(
        "--target-date", 
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Target date (YYYY-MM-DD, default: today)"
    )
    parser.add_argument(
        "--lookback-days", 
        type=int, 
        default=Config.LOOKBACK_DAYS,
        help=f"Number of days to look back (default: {Config.LOOKBACK_DAYS})"
    )
    parser.add_argument(
        "--max-reviews", 
        type=int, 
        default=Config.MAX_REVIEWS_PER_DAY,
        help=f"Maximum reviews per day (default: {Config.MAX_REVIEWS_PER_DAY})"
    )
    parser.add_argument(
        "--output-dir",
        default=Config.REPORTS_DIR,
        help=f"Output directory for reports (default: {Config.REPORTS_DIR})"
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    Config.ensure_directories()
    
    # Parse target date
    target_date = parse_date(args.target_date)
    start_date = target_date - timedelta(days=args.lookback_days)
    
    print("=" * 70)
    print("PLAY STORE TREND ANALYZER")
    print("=" * 70)
    print(f"📱 App: {Config.APP_ID}")
    print(f"📅 Analysis Period: {start_date.date()} to {target_date.date()}")
    print(f"📊 Lookback Days: {args.lookback_days}")
    print(f"📝 Max Reviews/Day: {args.max_reviews}")
    print("-" * 70)
    
    # Initialize components
    print("🔄 Initializing components...")
    orchestrator = TrendAnalysisOrchestrator()
    data_generator = MockDataGenerator()
    
    # Process data for each day
    print("\n📥 Processing review data...")
    print("-" * 70)
    
    current_date = start_date
    day_count = 0
    
    while current_date <= target_date:
        day_count += 1
        
        # Generate mock reviews for this day
        reviews = data_generator.generate_daily_reviews(
            current_date, 
            args.max_reviews
        )
        
        # Process the batch
        result = orchestrator.process_daily_batch(reviews, current_date)
        
        # Display progress
        if 'error' not in result:
            print(f"Day {day_count:2d}: {current_date.strftime('%Y-%m-%d')} - "
                  f"Processed {len(reviews):3d} reviews, "
                  f"Found {result.get('topic_count', 0):2d} topics")
        else:
            print(f"Day {day_count:2d}: {current_date.strftime('%Y-%m-%d')} - "
                  f"ERROR: {result.get('error', 'Unknown')}")
        
        current_date += timedelta(days=1)
    
    # Generate trend report
    print("\n" + "-" * 70)
    print("📈 Generating trend analysis report...")
    
    report = orchestrator.generate_trend_report(target_date)
    
    if report is not None and not report.empty:
        # Save reports
        csv_file, excel_file = save_reports(
            report, 
            target_date, 
            args.output_dir
        )
        
        # Print summary
        print_report_summary(report, target_date)
        
        print("\n" + "=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
        
    else:
        print("\n❌ Error: Could not generate trend report.")
        print("Please check the data and try again.")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())