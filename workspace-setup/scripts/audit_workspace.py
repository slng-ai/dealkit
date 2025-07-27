#!/usr/bin/env python3
"""
Automated Sales Workspace Audit Tool
Ensures structural integrity and separation of concerns
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class WorkspaceAuditor:
    """Audits workspace structure and enforces governance rules"""
    
    def __init__(self, workspace_root: str = '.'):
        self.root = Path(workspace_root)
        self.violations = defaultdict(list)
        self.warnings = defaultdict(list)
        self.stats = defaultdict(int)
        
    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete workspace audit"""
        print("🔍 Starting Sales Workspace Audit...")
        print("=" * 50)
        
        # Run all audit checks
        self.audit_directory_structure()
        self.audit_naming_conventions()
        self.audit_separation_of_concerns()
        self.audit_file_organization()
        self.audit_required_files()
        self.audit_security_boundaries()
        self.audit_depth_limits()
        
        # Generate report
        report = self.generate_report()
        
        # Save audit results
        self.save_audit_results(report)
        
        return report
    
    def audit_directory_structure(self):
        """Check top-level directory structure"""
        print("\n📁 Auditing directory structure...")
        
        required_dirs = [
            'customers',
            'reporting',
            'sales-toolkit',
            'workspace-setup',
            'personal',
            '.claude'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.root / dir_name
            if not dir_path.exists():
                self.violations['structure'].append(f"Missing required directory: {dir_name}")
            else:
                self.stats['directories_found'] += 1
        
        # Check for unauthorized top-level directories
        for item in self.root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if item.name not in required_dirs:
                    self.warnings['structure'].append(f"Unexpected top-level directory: {item.name}")
    
    def audit_naming_conventions(self):
        """Check naming convention compliance"""
        print("\n📝 Auditing naming conventions...")
        
        # Check folder naming (lowercase with hyphens)
        for folder in self.root.rglob('*'):
            if folder.is_dir() and not folder.name.startswith('.'):
                if '_' in folder.name and 'pycache' not in folder.name:
                    self.violations['naming'].append(f"Folder uses underscores: {folder.relative_to(self.root)}")
                if folder.name != folder.name.lower():
                    self.violations['naming'].append(f"Folder not lowercase: {folder.relative_to(self.root)}")
        
        # Check file naming conventions
        for file in self.root.rglob('*'):
            if file.is_file():
                if file.suffix == '.py':
                    # Python files should be snake_case
                    if not self._is_snake_case(file.stem):
                        self.violations['naming'].append(f"Python file not snake_case: {file.relative_to(self.root)}")
                
                elif file.suffix == '.md':
                    # System docs should be UPPERCASE, content should be lowercase-hyphenated
                    if file.parent == self.root:  # System docs in root
                        if file.stem != file.stem.upper():
                            self.violations['naming'].append(f"System doc not uppercase: {file.name}")
                    else:  # Content files
                        if not self._is_lowercase_hyphenated(file.stem) and file.stem != 'README':
                            self.warnings['naming'].append(f"Markdown file naming inconsistent: {file.relative_to(self.root)}")
                
                elif file.suffix == '.json':
                    # JSON files should be lowercase_underscore
                    if '-' in file.stem:
                        self.warnings['naming'].append(f"JSON file uses hyphens: {file.relative_to(self.root)}")
    
    def audit_separation_of_concerns(self):
        """Check for cross-boundary violations"""
        print("\n🚦 Auditing separation of concerns...")
        
        # Define allowed content patterns for each directory
        boundary_rules = {
            'customers': {
                'allowed': ['profile.json', 'notes', 'emails', 'slack', 'meetings', 'health_metrics.json'],
                'forbidden': ['*.py', 'template_*.md', 'config.json']
            },
            'sales-toolkit': {
                'allowed': ['*.md', 'templates', 'battlecards', 'playbooks', 'training'],
                'forbidden': ['*.py', 'profile.json', '*.log']
            },
            'reporting': {
                'allowed': ['*.py', 'README.md', '__init__.py'],
                'forbidden': ['profile.json', '*.json', 'template_*.md']
            },
            'workspace-setup': {
                'allowed': ['*.py', '*.json', '*.sh', 'README.md'],
                'forbidden': ['profile.json', 'template_*.md']
            }
        }
        
        for section, rules in boundary_rules.items():
            section_path = self.root / section
            if not section_path.exists():
                continue
                
            for file in section_path.rglob('*'):
                if file.is_file():
                    file_name = file.name
                    
                    # Check forbidden patterns
                    for forbidden in rules.get('forbidden', []):
                        if self._matches_pattern(file_name, forbidden):
                            self.violations['boundaries'].append(
                                f"Forbidden file in {section}: {file.relative_to(self.root)}"
                            )
    
    def audit_file_organization(self):
        """Check customer folder organization"""
        print("\n🗂️ Auditing file organization...")
        
        customers_dir = self.root / 'customers'
        if not customers_dir.exists():
            return
        
        for customer_dir in customers_dir.iterdir():
            if customer_dir.is_dir() and not customer_dir.name.startswith('.'):
                # Skip templates and workflows directories
                if customer_dir.name in ['templates', 'workflows']:
                    continue
                    
                # Check for required profile.json
                profile_path = customer_dir / 'profile.json'
                if not profile_path.exists():
                    self.violations['organization'].append(
                        f"Missing profile.json: {customer_dir.relative_to(self.root)}"
                    )
                else:
                    # Validate profile structure
                    try:
                        with open(profile_path, 'r') as f:
                            profile = json.load(f)
                            required_fields = ['company_name', 'industry', 'status']
                            for field in required_fields:
                                if field not in profile:
                                    self.warnings['organization'].append(
                                        f"Missing field '{field}' in {profile_path.relative_to(self.root)}"
                                    )
                    except json.JSONDecodeError:
                        self.violations['organization'].append(
                            f"Invalid JSON: {profile_path.relative_to(self.root)}"
                        )
                
                self.stats['customers_audited'] += 1
    
    def audit_required_files(self):
        """Check for required documentation files"""
        print("\n📄 Auditing required files...")
        
        required_files = {
            '.': ['README.md', 'MASTER_CONTEXT.md', 'QUICK_REFERENCE.md', 'PROJECT_AUDIT.md'],
            'reporting': ['README.md'],
            'reporting/personal': ['README.md'],
            'reporting/team': ['README.md'],
            'reporting/pulse': ['README.md'],
            'sales-toolkit': ['README.md'],
            'workspace-setup': ['README.md']
        }
        
        for path, files in required_files.items():
            dir_path = self.root / path
            if dir_path.exists():
                for file_name in files:
                    file_path = dir_path / file_name
                    if not file_path.exists():
                        self.violations['required_files'].append(
                            f"Missing required file: {file_path.relative_to(self.root)}"
                        )
    
    def audit_security_boundaries(self):
        """Check for security boundary violations"""
        print("\n🔐 Auditing security boundaries...")
        
        # Check for sensitive data in public areas
        public_areas = ['sales-toolkit']
        sensitive_patterns = ['api_key', 'password', 'token', 'secret', 'credential']
        
        for public_dir in public_areas:
            public_path = self.root / public_dir
            if not public_path.exists():
                continue
                
            for file in public_path.rglob('*'):
                if file.is_file() and file.suffix in ['.json', '.md', '.txt']:
                    try:
                        content = file.read_text().lower()
                        for pattern in sensitive_patterns:
                            if pattern in content:
                                self.violations['security'].append(
                                    f"Potential sensitive data in public area: {file.relative_to(self.root)}"
                                )
                                break
                    except:
                        pass
    
    def audit_depth_limits(self):
        """Check directory depth limits"""
        print("\n📏 Auditing depth limits...")
        
        depth_limits = {
            'customers': 3,
            'reporting': 2,
            'sales-toolkit/templates': 2,
            'workspace-setup/integrations': 3
        }
        
        for path, max_depth in depth_limits.items():
            base_path = self.root / path
            if not base_path.exists():
                continue
                
            for item in base_path.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(base_path)
                    depth = len(relative_path.parts)
                    if depth > max_depth:
                        self.violations['depth'].append(
                            f"Exceeds depth limit ({max_depth}): {item.relative_to(self.root)}"
                        )
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate audit report"""
        total_violations = sum(len(v) for v in self.violations.values())
        total_warnings = sum(len(v) for v in self.warnings.values())
        
        # Calculate health score
        health_score = 100
        health_score -= total_violations * 5  # Each violation costs 5 points
        health_score -= total_warnings * 2    # Each warning costs 2 points
        health_score = max(0, health_score)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'health_score': health_score,
            'summary': {
                'total_violations': total_violations,
                'total_warnings': total_warnings,
                'customers_audited': self.stats['customers_audited'],
                'directories_found': self.stats['directories_found']
            },
            'violations': dict(self.violations),
            'warnings': dict(self.warnings),
            'status': self._get_status(health_score)
        }
        
        return report
    
    def _get_status(self, score: int) -> str:
        """Get status based on health score"""
        if score >= 90:
            return 'EXCELLENT'
        elif score >= 80:
            return 'GOOD'
        elif score >= 70:
            return 'FAIR'
        else:
            return 'NEEDS_ATTENTION'
    
    def save_audit_results(self, report: Dict[str, Any]):
        """Save audit results to file"""
        audit_dir = self.root / 'audits'
        audit_dir.mkdir(exist_ok=True)
        
        filename = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        audit_file = audit_dir / filename
        
        with open(audit_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Audit results saved to: {audit_file.relative_to(self.root)}")
    
    def print_summary(self, report: Dict[str, Any]):
        """Print audit summary"""
        print("\n" + "=" * 50)
        print("📊 AUDIT SUMMARY")
        print("=" * 50)
        
        status_emoji = {
            'EXCELLENT': '🟢',
            'GOOD': '🟡',
            'FAIR': '🟠',
            'NEEDS_ATTENTION': '🔴'
        }
        
        print(f"\nHealth Score: {report['health_score']}/100 {status_emoji.get(report['status'], '⚫')}")
        print(f"Status: {report['status']}")
        print(f"\nViolations: {report['summary']['total_violations']}")
        print(f"Warnings: {report['summary']['total_warnings']}")
        
        # Print violations by category
        if report['violations']:
            print("\n🚨 VIOLATIONS:")
            for category, violations in report['violations'].items():
                if violations:
                    print(f"\n{category.upper()}:")
                    for v in violations[:5]:  # Show first 5
                        print(f"  ❌ {v}")
                    if len(violations) > 5:
                        print(f"  ... and {len(violations) - 5} more")
        
        # Print warnings by category
        if report['warnings']:
            print("\n⚠️ WARNINGS:")
            for category, warnings in report['warnings'].items():
                if warnings:
                    print(f"\n{category.upper()}:")
                    for w in warnings[:3]:  # Show first 3
                        print(f"  ⚠️ {w}")
                    if len(warnings) > 3:
                        print(f"  ... and {len(warnings) - 3} more")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if report['health_score'] < 80:
            print("  1. Review and fix all violations")
            print("  2. Address naming convention issues")
            print("  3. Ensure all required files are present")
        else:
            print("  ✅ Workspace structure is healthy!")
    
    def _is_snake_case(self, name: str) -> bool:
        """Check if name is snake_case"""
        return bool(re.match(r'^[a-z]+(_[a-z]+)*$', name))
    
    def _is_lowercase_hyphenated(self, name: str) -> bool:
        """Check if name is lowercase-hyphenated"""
        return bool(re.match(r'^[a-z]+(-[a-z]+)*$', name))
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern"""
        if pattern.startswith('*.'):
            return filename.endswith(pattern[1:])
        elif pattern.endswith('*'):
            return filename.startswith(pattern[:-1])
        else:
            return filename == pattern


def main():
    """Run workspace audit"""
    auditor = WorkspaceAuditor()
    report = auditor.run_full_audit()
    auditor.print_summary(report)
    
    # Return exit code based on health
    if report['health_score'] < 70:
        exit(1)  # Fail if health score is too low
    else:
        exit(0)  # Success


if __name__ == "__main__":
    main()