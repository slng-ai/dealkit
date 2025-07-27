#!/usr/bin/env python3
"""
Generate role-specific reports for a customer
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

from reports.fde_report import FDEReport
from reports.cro_report import CROReport
from reports.cfo_report import CFOReport
from reports.sdr_report import SDRReport

def main():
    parser = argparse.ArgumentParser(description='Generate role-specific customer reports')
    parser.add_argument('customer', help='Customer name')
    parser.add_argument('role', choices=['fde', 'cro', 'cfo', 'sdr', 'all'], 
                       help='Role to generate report for')
    parser.add_argument('--output', '-o', help='Output file (default: prints to console)')
    
    args = parser.parse_args()
    
    # Map roles to report classes
    report_classes = {
        'fde': FDEReport,
        'cro': CROReport,
        'cfo': CFOReport,
        'sdr': SDRReport
    }
    
    # Generate reports
    reports_to_generate = list(report_classes.keys()) if args.role == 'all' else [args.role]
    
    all_reports = []
    for role in reports_to_generate:
        print(f"\n📊 Generating {role.upper()} report for {args.customer}...\n")
        
        report_class = report_classes[role]
        report = report_class(args.customer)
        report_content = report.generate()
        
        if args.output and args.role != 'all':
            # Save to file if output specified and single role
            with open(args.output, 'w') as f:
                f.write(report_content)
            print(f"✅ Report saved to: {args.output}")
        else:
            # Print to console
            print(report_content)
            all_reports.append(f"# {role.upper()} Report\n\n{report_content}")
    
    # If generating all reports with output file, save them together
    if args.role == 'all' and args.output:
        with open(args.output, 'w') as f:
            f.write("\n\n---\n\n".join(all_reports))
        print(f"\n✅ All reports saved to: {args.output}")

if __name__ == "__main__":
    main()