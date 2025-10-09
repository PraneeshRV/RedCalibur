import argparse
import sys
import json
from datetime import datetime
from .config import Config, setup_logging
from .osint.domain_infrastructure.whois_lookup import perform_whois_lookup
from .osint.domain_infrastructure.dns_enumeration import enumerate_dns_records
from .osint.domain_infrastructure.subdomain_discovery import discover_subdomains
from .osint.domain_infrastructure.port_scanning import perform_port_scan
from .osint.domain_infrastructure.ssl_tls_details import get_ssl_details
from .osint.network_threat_intel.shodan_integration import perform_shodan_scan
from .osint.user_identity.username_lookup import lookup_username
from .osint.ai_enhanced.recon_summarizer import summarize_recon_data
from .osint.ai_enhanced.risk_scoring import calculate_risk_score
from .osint.ai_enhanced.report_generator import generate_pdf_report, generate_markdown_report
from .osint.virustotal_integration import scan_url
from .osint.search_engine_data_mining.google_dorking import perform_google_dorking
from .osint.image_file_osint.document_metadata_extraction import extract_document_metadata
from .osint.image_file_osint.exif_metadata_extraction import extract_exif_metadata

# New imports for enumeration and vulnerability scanning
from .enumeration.service_detector import detect_services, fingerprint_service
from .enumeration.banner_grabber import grab_banner
from .enumeration.directory_enumeration import enumerate_directories, quick_scan
from .vulnerability_scanning.cve_scanner import scan_for_cves
from .vulnerability_scanning.service_vuln_check import check_service_vulnerabilities, batch_check_services

class RedCaliburCLI:
    """Professional CLI interface for RedCalibur"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.config = Config()
        
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="RedCalibur - AI-Powered Red Teaming Toolkit",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Reconnaissance
  redcalibur domain --target example.com --all
  redcalibur scan --target 192.168.1.1 --ports 80,443,22
  redcalibur username --target johndoe --platforms twitter,linkedin
  
  # Enumeration
  redcalibur enumerate --target 192.168.1.1 --banner
  redcalibur enumerate --target example.com --dir-enum http://example.com
  
  # Vulnerability Scanning
  redcalibur vuln-scan --software apache --version 2.4.41
  redcalibur vuln-scan --target 192.168.1.1 --ports 80,443,22
  redcalibur vuln-scan --cve-id CVE-2021-44228
  
  # Automated Pentest
  redcalibur auto-pentest --target 192.168.1.1 --domain example.com
  
  # Reports & Utilities
  redcalibur report --input data.json --format pdf
  redcalibur urlscan --url http://example.com
  redcalibur file-osint extract-doc-meta --path /path/to/document.pdf
  redcalibur auto-recon
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Domain reconnaissance
        domain_parser = subparsers.add_parser('domain', help='Domain reconnaissance')
        domain_parser.add_argument('--target', required=True, help='Target domain')
        domain_parser.add_argument('--whois', action='store_true', help='Perform WHOIS lookup')
        domain_parser.add_argument('--dns', action='store_true', help='Enumerate DNS records')
        domain_parser.add_argument('--subdomains', action='store_true', help='Discover subdomains')
        domain_parser.add_argument('--ssl', action='store_true', help='Get SSL/TLS details')
        domain_parser.add_argument('--all', action='store_true', help='Run all domain checks')
        
        # Network scanning
        scan_parser = subparsers.add_parser('scan', help='Network scanning')
        scan_parser.add_argument('--target', required=True, help='Target IP or domain')
        scan_parser.add_argument('--ports', help='Comma-separated list of ports (default: common ports)')
        scan_parser.add_argument('--shodan', action='store_true', help='Use Shodan scan')
        
        # Username lookup
        username_parser = subparsers.add_parser('username', help='Username reconnaissance')
        username_parser.add_argument('--target', required=True, help='Target username')
        username_parser.add_argument('--platforms', help='Comma-separated platforms to check')
        
        # Report generation
        report_parser = subparsers.add_parser('report', help='Generate reports')
        report_parser.add_argument('--input', required=True, help='Input JSON file with results')
        report_parser.add_argument('--format', choices=['pdf', 'json', 'both'], default='both')
        report_parser.add_argument('--output', help='Output filename (without extension)')
        
        # Configuration
        config_parser = subparsers.add_parser('config', help='Configuration management')
        config_parser.add_argument('--check', action='store_true', help='Check configuration')
        config_parser.add_argument('--show', action='store_true', help='Show current configuration')
        
        # All-in-one command
        all_parser = subparsers.add_parser('all', help='Run all functionalities and generate a summary report')
        all_parser.add_argument('--target-domain', required=True, help='Target domain for reconnaissance')
        all_parser.add_argument('--target-ip', required=True, help='Target IP for network scanning')
        all_parser.add_argument('--username', required=True, help='Target username for lookup')
        all_parser.add_argument('--platforms', help='Comma-separated platforms for username lookup', default='twitter,linkedin,github,instagram')
        all_parser.add_argument('--output', help='Output filename (without extension)', default='redcalibur_summary')
        
        # URL scanning
        urlscan_parser = subparsers.add_parser('urlscan', help='Scan a URL using VirusTotal API')
        urlscan_parser.add_argument('--url', required=True, help='URL to scan')

        # Automated Reconnaissance
        subparsers.add_parser('auto-recon', help='Run a fully automated, interactive OSINT process')

        # File-based OSINT
        file_osint_parser = subparsers.add_parser('file-osint', help='OSINT on local files')
        file_osint_subparsers = file_osint_parser.add_subparsers(dest='file_command', help='File OSINT commands')

        doc_meta_parser = file_osint_subparsers.add_parser('extract-doc-meta', help='Extract metadata from documents (PDF)')
        doc_meta_parser.add_argument('--path', required=True, help='Path to the document file')

        exif_parser = file_osint_subparsers.add_parser('extract-exif', help='Extract EXIF data from images')
        exif_parser.add_argument('--path', required=True, help='Path to the image file')

        # Enumeration commands
        enum_parser = subparsers.add_parser('enumerate', help='Service enumeration and fingerprinting')
        enum_parser.add_argument('--target', required=True, help='Target IP or hostname')
        enum_parser.add_argument('--ports', help='Comma-separated list of ports (default: common ports)')
        enum_parser.add_argument('--banner', action='store_true', help='Grab service banners')
        enum_parser.add_argument('--dir-enum', help='Enumerate directories on web server (provide base URL)')
        
        # Vulnerability scanning commands
        vuln_parser = subparsers.add_parser('vuln-scan', help='Vulnerability scanning')
        vuln_parser.add_argument('--software', help='Software name to scan for CVEs')
        vuln_parser.add_argument('--version', help='Software version (optional)')
        vuln_parser.add_argument('--target', help='Target to scan services and check vulnerabilities')
        vuln_parser.add_argument('--ports', help='Ports to scan on target (comma-separated)')
        vuln_parser.add_argument('--cve-id', help='Look up specific CVE by ID')
        
        # Automated pentest command
        pentest_parser = subparsers.add_parser('auto-pentest', help='Automated penetration testing workflow')
        pentest_parser.add_argument('--target', required=True, help='Target IP or hostname')
        pentest_parser.add_argument('--domain', help='Target domain (optional)')
        pentest_parser.add_argument('--output', help='Output filename prefix', default='pentest_report')

        return parser.parse_args()
    
    def run_domain_recon(self, args):
        """Run domain reconnaissance"""
        results = {"target": args.target, "timestamp": datetime.now().isoformat()}
        
        try:
            if args.whois or args.all:
                self.logger.info(f"Performing WHOIS lookup for {args.target}")
                results["whois"] = perform_whois_lookup(args.target)
                
            if args.dns or args.all:
                self.logger.info(f"Enumerating DNS records for {args.target}")
                results["dns"] = enumerate_dns_records(args.target)
                
            if args.subdomains or args.all:
                self.logger.info(f"Discovering subdomains for {args.target}")
                results["subdomains"] = discover_subdomains(args.target, self.config.SUBDOMAIN_WORDLIST)
                
            if args.ssl or args.all:
                self.logger.info(f"Getting SSL/TLS details for {args.target}")
                results["ssl"] = get_ssl_details(args.target)
                
            # AI Enhancement: Summarize results
            if args.all:
                raw_data = json.dumps(results, indent=2, default=str)
                summary = summarize_recon_data(raw_data[:1000])  # Truncate for summarization
                results["ai_summary"] = summary
                
                # Calculate risk score
                features = [
                    len(results.get("subdomains", [])),
                    1 if "error" not in results.get("ssl", {}) else 0,
                    len(results.get("dns", {}).get("A", []))
                ]
                risk_score = calculate_risk_score(features)
                results["risk_score"] = risk_score
                
        except Exception as e:
            self.logger.error(f"Error in domain reconnaissance: {str(e)}")
            results["error"] = str(e)
            
        return results
    
    def run_network_scan(self, args):
        """Run network scanning"""
        results = {"target": args.target, "timestamp": datetime.now().isoformat()}
        
        try:
            if args.ports:
                ports = [int(p.strip()) for p in args.ports.split(',')]
            else:
                ports = self.config.DEFAULT_PORTS
                
            self.logger.info(f"Scanning ports {ports} on {args.target}")
            results["port_scan"] = perform_port_scan(args.target, ports)
            
            if args.shodan and self.config.SHODAN_API_KEY:
                self.logger.info(f"Performing Shodan scan on {args.target}")
                results["shodan"] = perform_shodan_scan(self.config.SHODAN_API_KEY, args.target)
            elif args.shodan:
                self.logger.warning("Shodan API key not configured")
                
        except Exception as e:
            self.logger.error(f"Error in network scanning: {str(e)}")
            results["error"] = str(e)
            
        return results
    
    def run_username_lookup(self, args):
        """Run username reconnaissance"""
        results = {"target": args.target, "timestamp": datetime.now().isoformat()}
        
        try:
            if args.platforms:
                platforms = [p.strip() for p in args.platforms.split(',')]
            else:
                platforms = ["twitter", "linkedin", "github", "instagram"]
                
            self.logger.info(f"Looking up username {args.target} on platforms: {platforms}")
            results["username_lookup"] = lookup_username(args.target, platforms)
            
        except Exception as e:
            self.logger.error(f"Error in username lookup: {str(e)}")
            results["error"] = str(e)
            
        return results
    
    def generate_report(self, args):
        """Generate reports from results"""
        try:
            with open(args.input, 'r') as f:
                data = json.load(f)
                
            output_name = args.output or f"redcalibur_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if args.format in ['pdf', 'both']:
                pdf_path = f"{self.config.OUTPUT_DIR}/{output_name}.pdf"
                generate_pdf_report(data, pdf_path)
                self.logger.info(f"PDF report generated: {pdf_path}")

            if args.format in ['json', 'both']:
                json_path = f"{self.config.OUTPUT_DIR}/{output_name}.json"
                with open(json_path, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                self.logger.info(f"JSON report generated: {json_path}")

            # Always generate Markdown report
            from .osint.ai_enhanced.report_generator import generate_markdown_report
            md_path = f"{self.config.OUTPUT_DIR}/{output_name}.md"
            generate_markdown_report(data, md_path)
            self.logger.info(f"Markdown report generated: {md_path}")
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            
    def check_config(self):
        """Check configuration"""
        issues = self.config.validate_config()
        
        if issues:
            self.logger.warning("Configuration issues found:")
            for issue in issues:
                self.logger.warning(f"  - {issue}")
        else:
            self.logger.info("Configuration is valid")
            
    def show_config(self):
        """Show current configuration"""
        config_info = {
            "SHODAN_API_KEY": "Set" if self.config.SHODAN_API_KEY else "Not set",
            "GEMINI_API_KEY": "Set" if self.config.GEMINI_API_KEY else "Not set",
            "OUTPUT_DIR": self.config.OUTPUT_DIR,
            "REPORT_FORMAT": self.config.REPORT_FORMAT,
            "DEFAULT_PORTS": self.config.DEFAULT_PORTS
        }
        
        print(json.dumps(config_info, indent=2))
    
    def run_all(self, args):
        """Run all functionalities and generate a summary report"""
        results = {
            "domain": self.run_domain_recon(argparse.Namespace(
                target=args.target_domain, whois=True, dns=True, subdomains=True, ssl=True, all=True
            )),
            "network": self.run_network_scan(argparse.Namespace(
                target=args.target_ip, ports=None, shodan=True
            )),
            "username": self.run_username_lookup(argparse.Namespace(
                target=args.username, platforms=args.platforms.split(',')
            ))
        }

        # Summarize results using Gemini API
        try:
            raw_data = json.dumps(results, indent=2)
            self.logger.info("Summarizing results using Gemini API")
            summary = summarize_recon_data(raw_data[:1000])  # Truncate for summarization
            results["gemini_summary"] = summary
        except Exception as e:
            self.logger.error(f"Error summarizing results with Gemini API: {str(e)}")
            results["gemini_summary_error"] = str(e)


        # Generate user-friendly reports (PDF, JSON, and Markdown)
        output_name = f"{self.config.OUTPUT_DIR}/{args.output}"
        try:
            self.logger.info("Generating user-friendly report")
            generate_pdf_report(results, f"{output_name}.pdf")
            with open(f"{output_name}.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            # Always generate Markdown report
            from .osint.ai_enhanced.report_generator import generate_markdown_report
            generate_markdown_report(results, f"{output_name}.md")
            self.logger.info(f"Reports generated: {output_name}.pdf, {output_name}.json, {output_name}.md")
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")

        print(json.dumps(results, indent=2, default=str))
    
    def run_url_scan(self, args):
        """Scan a URL using VirusTotal API"""
        results = {"url": args.url, "timestamp": datetime.now().isoformat()}

        try:
            self.logger.info(f"Scanning URL: {args.url}")
            scan_results = scan_url(self.config.VIRUSTOTAL_API_KEY, args.url)
            if scan_results:
                results.update(scan_results)
            else:
                results["error"] = "Failed to scan URL"
        except Exception as e:
            self.logger.error(f"Error scanning URL: {str(e)}")
            results["error"] = str(e)

        print(json.dumps(results, indent=2, default=str))
        return results
    
    def get_targets_interactively(self):
        """Get target information from the user interactively"""
        print("Starting fully automated OSINT process...")
        target_domain = input("Enter the target domain (e.g., example.com): ")
        target_ip = input("Enter the target IP address: ")
        return target_domain, target_ip

    def run_auto_recon(self):
        """Run a fully automated, interactive OSINT process"""
        target_domain, target_ip = self.get_targets_interactively()

        results = {
            "domain": self.run_domain_recon(argparse.Namespace(
                target=target_domain, whois=True, dns=True, subdomains=True, ssl=True, all=True
            )),
            "network": self.run_network_scan(argparse.Namespace(
                target=target_ip, ports=None, shodan=True
            )),
            "url_scan": self.run_url_scan(argparse.Namespace(url=f"http://{target_domain}"))
        }

        # Add Google Dorking
        try:
            self.logger.info(f"Performing Google Dorking for {target_domain}")
            dork_queries = [
                f'site:{target_domain} intitle:"index of"',
                f'site:{target_domain} filetype:pdf',
                f'site:{target_domain} inurl:login'
            ]
            results["google_dorking"] = {}
            for query in dork_queries:
                results["google_dorking"][query] = perform_google_dorking(query)
        except Exception as e:
            self.logger.error(f"Error during Google Dorking: {str(e)}")
            results["google_dorking_error"] = str(e)

        # Summarize results using Gemini API
        try:
            raw_data = json.dumps(results, indent=2, default=str)
            self.logger.info("Summarizing results using Gemini API for a comprehensive report")
            summary = summarize_recon_data(raw_data)
            results["gemini_summary"] = summary
        except Exception as e:
            self.logger.error(f"Error summarizing results with Gemini API: {str(e)}")
            results["gemini_summary_error"] = str(e)

        # Generate final report
        output_name = f"{self.config.OUTPUT_DIR}/automated_recon_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            self.logger.info("Generating final reconnaissance report")
            generate_markdown_report(results, f"{output_name}.md")
            with open(f"{output_name}.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.info(f"Automated reconnaissance report generated: {output_name}.md")
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")

        print(json.dumps(results, indent=2, default=str))
    
    def run_file_osint(self, args):
        """Run file-based OSINT"""
        results = {}
        if args.file_command == 'extract-doc-meta':
            self.logger.info(f"Extracting metadata from {args.path}")
            results = extract_document_metadata(args.path)
        elif args.file_command == 'extract-exif':
            self.logger.info(f"Extracting EXIF data from {args.path}")
            results = extract_exif_metadata(args.path)

        output_file = f"{self.config.OUTPUT_DIR}/file_osint_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
                
        print(json.dumps(results, indent=2, default=str))
        self.logger.info(f"Results saved to {output_file}")

    def run_enumeration(self, args):
        """Run service enumeration"""
        results = {
            "target": args.target,
            "timestamp": datetime.now().isoformat(),
            "services": []
        }
        
        try:
            # Determine ports to scan
            if args.ports:
                ports = [int(p.strip()) for p in args.ports.split(',')]
            else:
                ports = self.config.DEFAULT_PORTS
            
            self.logger.info(f"Enumerating services on {args.target}")
            
            # Detect services
            services = detect_services(args.target, ports)
            results["services"] = services
            results["total_services"] = len(services)
            
            # Grab banners if requested
            if args.banner:
                self.logger.info("Grabbing service banners...")
                for service in services:
                    if service.get("state") == "open":
                        banner_result = grab_banner(args.target, service["port"])
                        if banner_result.get("success"):
                            service["detailed_banner"] = banner_result["banner"]
            
            # Directory enumeration if URL provided
            if args.dir_enum:
                self.logger.info(f"Enumerating directories on {args.dir_enum}")
                dir_results = quick_scan(args.dir_enum)
                results["directory_enum"] = dir_results
            
        except Exception as e:
            self.logger.error(f"Error in enumeration: {str(e)}")
            results["error"] = str(e)
        
        # Save results
        output_file = f"{self.config.OUTPUT_DIR}/enumeration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(json.dumps(results, indent=2, default=str))
        self.logger.info(f"Enumeration results saved to {output_file}")
        
        return results
    
    def run_vulnerability_scan(self, args):
        """Run vulnerability scanning"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": []
        }
        
        try:
            # Scan by software name
            if args.software:
                self.logger.info(f"Scanning for CVEs in {args.software} {args.version or ''}")
                cve_results = scan_for_cves(args.software, args.version)
                results["software"] = args.software
                results["version"] = args.version
                results["cves"] = cve_results.get("cves", [])
                results["total_cves"] = cve_results.get("total_found", 0)
                results["severity_counts"] = {
                    "critical": cve_results.get("critical_count", 0),
                    "high": cve_results.get("high_count", 0),
                    "medium": cve_results.get("medium_count", 0),
                    "low": cve_results.get("low_count", 0)
                }
                
                if "error" in cve_results:
                    results["error"] = cve_results["error"]
            
            # Scan target with service detection
            elif args.target:
                self.logger.info(f"Scanning {args.target} for vulnerabilities")
                results["target"] = args.target
                
                # First, enumerate services
                if args.ports:
                    ports = [int(p.strip()) for p in args.ports.split(',')]
                else:
                    ports = self.config.DEFAULT_PORTS
                
                services = detect_services(args.target, ports)
                self.logger.info(f"Found {len(services)} services")
                
                # Check vulnerabilities for each service
                vuln_results = batch_check_services(services)
                results["services"] = vuln_results
                
                # Count total vulnerabilities
                total_vulns = sum(s.get("total_cves", 0) for s in vuln_results)
                results["total_vulnerabilities"] = total_vulns
            
            # Look up specific CVE
            elif args.cve_id:
                from .vulnerability_scanning.cve_scanner import search_cve_by_id
                self.logger.info(f"Looking up {args.cve_id}")
                cve_data = search_cve_by_id(args.cve_id)
                results["cve_id"] = args.cve_id
                results["cve_data"] = cve_data
            
        except Exception as e:
            self.logger.error(f"Error in vulnerability scan: {str(e)}")
            results["error"] = str(e)
        
        # Save results
        output_file = f"{self.config.OUTPUT_DIR}/vulnerability_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(json.dumps(results, indent=2, default=str))
        self.logger.info(f"Vulnerability scan results saved to {output_file}")
        
        return results
    
    def run_automated_pentest(self, args):
        """Run automated penetration testing workflow"""
        self.logger.info(f"Starting automated pentest on {args.target}")
        
        results = {
            "target": args.target,
            "domain": args.domain,
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }
        
        try:
            # Phase 1: Reconnaissance
            self.logger.info("Phase 1: Reconnaissance")
            if args.domain:
                recon_results = self.run_domain_recon(argparse.Namespace(
                    target=args.domain,
                    whois=True,
                    dns=True,
                    subdomains=True,
                    ssl=True,
                    all=True
                ))
                results["phases"]["reconnaissance"] = recon_results
            
            # Phase 2: Enumeration
            self.logger.info("Phase 2: Service Enumeration")
            enum_results = self.run_enumeration(argparse.Namespace(
                target=args.target,
                ports=None,
                banner=True,
                dir_enum=f"http://{args.target}" if not args.target.startswith('http') else args.target
            ))
            results["phases"]["enumeration"] = enum_results
            
            # Phase 3: Vulnerability Scanning
            self.logger.info("Phase 3: Vulnerability Scanning")
            vuln_results = self.run_vulnerability_scan(argparse.Namespace(
                software=None,
                version=None,
                target=args.target,
                ports=None,
                cve_id=None
            ))
            results["phases"]["vulnerability_scan"] = vuln_results
            
            # Phase 4: Risk Assessment Summary
            self.logger.info("Phase 4: Generating Risk Assessment")
            total_vulns = vuln_results.get("total_vulnerabilities", 0)
            open_ports = len([s for s in enum_results.get("services", []) if s.get("state") == "open"])
            
            results["risk_summary"] = {
                "total_vulnerabilities": total_vulns,
                "open_ports": open_ports,
                "risk_level": "HIGH" if total_vulns > 10 else "MEDIUM" if total_vulns > 0 else "LOW"
            }
            
        except Exception as e:
            self.logger.error(f"Error in automated pentest: {str(e)}")
            results["error"] = str(e)
        
        # Generate comprehensive report
        output_name = f"{self.config.OUTPUT_DIR}/{args.output}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Save JSON
            with open(f"{output_name}.json", 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            # Generate Markdown report
            generate_markdown_report(results, f"{output_name}.md")
            
            self.logger.info(f"Automated pentest complete. Reports saved: {output_name}")
            
        except Exception as e:
            self.logger.error(f"Error generating pentest report: {str(e)}")
        
        print(json.dumps(results, indent=2, default=str))
        
        return results

    def run(self):
        """Main CLI entry point"""
        args = self.parse_arguments()
        
        if not args.command:
            print("No command specified. Use --help for usage information.")
            sys.exit(1)
            
        if args.command == 'config':
            if args.check:
                self.check_config()
            elif args.show:
                self.show_config()
            return
            
        results = None
        
        if args.command == 'domain':
            results = self.run_domain_recon(args)
        elif args.command == 'scan':
            results = self.run_network_scan(args)
        elif args.command == 'username':
            results = self.run_username_lookup(args)
        elif args.command == 'report':
            self.generate_report(args)
            return
        elif args.command == 'all':
            self.run_all(args)
            return
        elif args.command == 'urlscan':
            results = self.run_url_scan(args)
            return
        elif args.command == 'auto-recon':
            self.run_auto_recon()
            return
        elif args.command == 'file-osint':
            self.run_file_osint(args)
            return
        elif args.command == 'enumerate':
            results = self.run_enumeration(args)
            return
        elif args.command == 'vuln-scan':
            results = self.run_vulnerability_scan(args)
            return
        elif args.command == 'auto-pentest':
            results = self.run_automated_pentest(args)
            return
            
        if results:
            # Save results to file
            output_file = f"{self.config.OUTPUT_DIR}/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
                
            print(json.dumps(results, indent=2, default=str))
            self.logger.info(f"Results saved to {output_file}")

def main():
    """Entry point for the CLI"""
    cli = RedCaliburCLI()
    cli.run()

if __name__ == "__main__":
    main()
