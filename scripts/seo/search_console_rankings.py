# search_console_rankings.py

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
import os.path
import pickle
from datetime import datetime, timedelta

# Scopes required
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def authenticate():
    """Authenticate with Google Search Console API"""
    creds = None
    
    # Token file stores access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_search_analytics(service, site_url, start_date, end_date):
    """Pull search analytics data from Search Console"""
    
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query', 'page'],
        'rowLimit': 1000,
        'startRow': 0
    }
    
    response = service.searchanalytics().query(
        siteUrl=site_url, 
        body=request
    ).execute()
    
    return response.get('rows', [])

def format_rankings_report(data, start_date, end_date):
    """Format data into readable report"""
    
    report = f"""
# Azure-Noob Rankings Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: {start_date} to {end_date}

## Summary Statistics

Total Queries: {len(data)}
"""
    
    # Calculate totals
    total_clicks = sum(row.get('clicks', 0) for row in data)
    total_impressions = sum(row.get('impressions', 0) for row in data)
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    
    report += f"""
Total Clicks: {total_clicks}
Total Impressions: {total_impressions}
Average CTR: {avg_ctr:.2f}%

## Top Queries by Impressions

"""
    
    # Sort by impressions
    sorted_data = sorted(data, key=lambda x: x.get('impressions', 0), reverse=True)
    
    for i, row in enumerate(sorted_data[:50], 1):
        query = row['keys'][0]
        page = row['keys'][1] if len(row['keys']) > 1 else 'N/A'
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0) * 100
        position = row.get('position', 0)
        
        report += f"""
### {i}. {query}
- Position: {position:.1f}
- Clicks: {clicks}
- Impressions: {impressions}
- CTR: {ctr:.2f}%
- Page: {page.replace('https://azure-noob.com', '')}
"""
    
    # Opportunity analysis
    report += "\n\n## 🎯 Optimization Opportunities\n\n"
    
    # High impressions, low CTR
    report += "### High Impressions, Low CTR (<2%)\n"
    low_ctr = [r for r in data if r.get('impressions', 0) > 50 and r.get('ctr', 0) < 0.02]
    if low_ctr:
        for row in sorted(low_ctr, key=lambda x: x.get('impressions', 0), reverse=True)[:10]:
            query = row['keys'][0]
            impressions = row.get('impressions', 0)
            ctr = row.get('ctr', 0) * 100
            position = row.get('position', 0)
            report += f"- **{query}** - Pos {position:.1f}, {impressions} imp, {ctr:.2f}% CTR\n"
    else:
        report += "None found\n"
    
    # Positions 11-30 (opportunity zone)
    report += "\n### Positions 11-30 (Push to Page 1)\n"
    opportunity = [r for r in data if 11 <= r.get('position', 0) <= 30]
    if opportunity:
        for row in sorted(opportunity, key=lambda x: x.get('impressions', 0), reverse=True)[:10]:
            query = row['keys'][0]
            impressions = row.get('impressions', 0)
            position = row.get('position', 0)
            clicks = row.get('clicks', 0)
            report += f"- **{query}** - Pos {position:.1f}, {impressions} imp, {clicks} clicks\n"
    else:
        report += "None found\n"
    
    # Top 10 positions (protect these)
    report += "\n### Top 10 Positions (Maintain Rankings)\n"
    top_10 = [r for r in data if r.get('position', 0) <= 10]
    if top_10:
        for row in sorted(top_10, key=lambda x: x.get('position', 0))[:10]:
            query = row['keys'][0]
            position = row.get('position', 0)
            clicks = row.get('clicks', 0)
            impressions = row.get('impressions', 0)
            report += f"- **{query}** - Pos {position:.1f}, {clicks} clicks, {impressions} imp\n"
    else:
        report += "None found\n"
    
    return report

def main():
    """Main execution"""
    
    # Your site URL - try both formats
    SITE_URL = 'sc-domain:azure-noob.com'
    
    # Date range (last 7 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    print("Authenticating with Google Search Console...")
    creds = authenticate()
    service = build('searchconsole', 'v1', credentials=creds)
    
    print(f"Pulling data from {start_date} to {end_date}...")
    
    try:
        data = get_search_analytics(
            service, 
            SITE_URL, 
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
    except Exception as e:
        print(f"Error with sc-domain format, trying https:// format...")
        SITE_URL = 'https://azure-noob.com/'
        data = get_search_analytics(
            service, 
            SITE_URL, 
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
    
    print(f"Retrieved {len(data)} rows")
    
    if len(data) == 0:
        print("\nNo data retrieved. This could mean:")
        print("1. No search traffic in this period")
        print("2. Search Console property not verified")
        print("3. Wrong site URL format")
        print("\nTry verifying your site in Search Console first.")
        return
    
    # Generate report
    report = format_rankings_report(
        data, 
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    # Save to file
    report_file = f"rankings_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Report saved to: {report_file}")
    print("\nFirst 50 lines of report:")
    print("=" * 80)
    print('\n'.join(report.split('\n')[:50]))

if __name__ == '__main__':
    main()