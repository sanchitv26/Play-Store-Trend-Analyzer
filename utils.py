"""
Utility functions for trend analysis
"""
import pandas as pd
import os
from datetime import datetime
from typing import Dict, Any

def create_summary_sheet(report: pd.DataFrame) -> pd.DataFrame:
    """Create summary statistics sheet"""
    summary_data = {
        'Metric': [
            'Total Topics Tracked',
            'Total Mentions',
            'Average Daily Mentions',
            'Most Frequent Topic',
            'Least Frequent Topic',
            'Topics with Significant Growth',
            'New Topics (Last 7 days)'
        ],
        'Value': [
            len(report),
            int(report.sum().sum()),
            round(report.sum(axis=1).mean(), 2),
            report.sum(axis=1).idxmax() if len(report) > 0 else 'N/A',
            report.sum(axis=1).idxmin() if len(report) > 0 else 'N/A',
            calculate_growth_topics(report),
            identify_new_topics(report)
        ]
    }
    return pd.DataFrame(summary_data)

def calculate_growth_topics(report: pd.DataFrame, threshold: float = 0.3) -> int:
    """Calculate number of topics with significant growth"""
    if len(report.columns) < 7:
        return 0
    
    last_week = report.columns[-7:].tolist()
    prev_week = report.columns[-14:-7].tolist() if len(report.columns) >= 14 else report.columns[:7].tolist()
    
    growth_count = 0
    for _, row in report.iterrows():
        last_avg = row[last_week].mean()
        prev_avg = row[prev_week].mean() if prev_week else 0
        
        if prev_avg > 0 and (last_avg - prev_avg) / prev_avg > threshold:
            growth_count += 1
    
    return growth_count

def identify_new_topics(report: pd.DataFrame) -> int:
    """Identify topics that appeared in the last 7 days"""
    if len(report.columns) < 7:
        return 0
    
    last_week = report.columns[-7:].tolist()
    new_topics = 0
    
    for _, row in report.iterrows():
        last_week_sum = row[last_week].sum()
        
        if len(report.columns) > 7:
            before_week = report.columns[:-7].tolist()
            before_sum = row[before_week].sum()
            if last_week_sum > 0 and before_sum == 0:
                new_topics += 1
        elif last_week_sum > 0:
            new_topics += 1
    
    return new_topics

def identify_trending_topics(report: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Identify top trending topics"""
    if len(report.columns) < 7:
        return pd.DataFrame()
    
    # Calculate growth rate
    growth_data = []
    last_week = report.columns[-7:].tolist()
    prev_week = report.columns[-14:-7].tolist() if len(report.columns) >= 14 else report.columns[:7].tolist()
    
    for topic, row in report.iterrows():
        last_avg = row[last_week].mean()
        prev_avg = row[prev_week].mean() if prev_week else 0
        
        if prev_avg > 0:
            growth_rate = (last_avg - prev_avg) / prev_avg
        else:
            growth_rate = last_avg if last_avg > 0 else 0
        
        growth_data.append({
            'Topic': topic,
            'Last Week Avg': round(last_avg, 2),
            'Prev Week Avg': round(prev_avg, 2),
            'Growth Rate': round(growth_rate, 2),
            'Growth %': f"{round(growth_rate * 100, 1)}%",
            'Total Mentions': int(row.sum())
        })
    
    df = pd.DataFrame(growth_data)
    df = df.sort_values('Growth Rate', ascending=False).head(top_n)
    return df

def print_report_summary(report: pd.DataFrame, target_date: datetime):
    """Print summary of the analysis"""
    print("\n" + "=" * 70)
    print("TREND ANALYSIS REPORT SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 Basic Statistics:")
    print(f"   • Analysis Period: {len(report.columns)} days")
    print(f"   • Total Topics Tracked: {len(report)}")
    print(f"   • Total Mentions: {report.sum().sum():,}")
    
    # Top 5 topics
    print(f"\n🏆 Top 5 Most Frequent Topics:")
    top_topics = report.sum(axis=1).sort_values(ascending=False).head(5)
    for i, (topic, count) in enumerate(top_topics.items(), 1):
        print(f"   {i}. {topic}: {int(count)} mentions")
    
    # Trending topics
    if len(report.columns) >= 7:
        trending_df = identify_trending_topics(report, top_n=5)
        if not trending_df.empty:
            print(f"\n📈 Top 5 Trending Topics (Week over Week):")
            for i, row in trending_df.iterrows():
                growth = row['Growth Rate']
                arrow = "↑" if growth > 0 else "↓"
                print(f"   • {row['Topic']}: {row['Growth %']} {arrow}")

def save_reports(report: pd.DataFrame, target_date: datetime, output_dir: str):
    """Save reports in CSV and Excel formats"""
    date_str = target_date.strftime("%Y%m%d")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # CSV format
    csv_file = os.path.join(output_dir, f"trend_report_{date_str}.csv")
    report.to_csv(csv_file)
    print(f"\n📄 CSV Report saved: {csv_file}")
    
    # Excel format with multiple sheets
    excel_file = os.path.join(output_dir, f"trend_report_{date_str}.xlsx")
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Main trend data
        report.to_excel(writer, sheet_name='Trend Analysis')
        
        # Summary sheet
        summary_df = create_summary_sheet(report)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Trending topics sheet
        trending_df = identify_trending_topics(report, top_n=15)
        trending_df.to_excel(writer, sheet_name='Trending Topics', index=False)
        
        # Top topics sheet
        top_topics = report.sum(axis=1).sort_values(ascending=False).head(20)
        top_topics_df = pd.DataFrame({
            'Topic': top_topics.index,
            'Total Mentions': top_topics.values,
            'Average Daily': [round(val/len(report.columns), 2) for val in top_topics.values]
        })
        top_topics_df.to_excel(writer, sheet_name='Top Topics', index=False)
    
    print(f"📊 Excel Report saved: {excel_file}")
    
    return csv_file, excel_file