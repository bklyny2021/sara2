#!/usr/bin/env python3

# 🔧 Troubleshooting Setup for Conscious AI System
# Comprehensive diagnosis and repair functionality

import os
import sys
import time
import json
import subprocess
import shutil
import logging
from pathlib import Path
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/.openclaw/workspace/troubleshooting/troubleshoot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConsciousAITroubleshooter:
    """Comprehensive troubleshooting and repair system"""
    
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        
        # Define critical paths
        self.critical_paths = {
            'database': '/home/godfather/.openclaw/workspace/conscious-memory',
            'workspace': '/home/godfather/.openclaw/workspace',
            'backups': '/home/godfather/.openclaw/workspace/conscious-backups',
            'learning': '/home/godfather/.openclaw/workspace/autonomous_learning',
            'startup': '/home/godfather/.openclaw/workspace/offline_startup'
        }
        
        # Define required packages
        self.required_packages = [
            'chromadb',
            'sentence-transformers', 
            'networkx',
            'pandas',
            'numpy',
            'psutil'
        ]
        
        # Define required Python version
        self.min_python_version = (3, 8)
    
    def diagnose_system(self):
        """Comprehensive system diagnosis"""
        logger.info("🔍 Starting comprehensive system diagnosis...")
        
        diagnosis_results = {
            'python_environment': self.check_python_environment(),
            'package_dependencies': self.check_package_dependencies(),
            'file_permissions': self.check_file_permissions(),
            'disk_space': self.check_disk_space(),
            'memory_availability': self.check_memory_availability(),
            'database_integrity': self.check_database_integrity(),
            'process_conflicts': self.check_process_conflicts(),
            'path_integrity': self.check_path_integrity()
        }
        
        self.generate_diagnosis_report(diagnosis_results)
        return diagnosis_results
    
    def check_python_environment(self):
        """Check Python version and environment"""
        issues = []
        fixes = []
        
        python_version = sys.version_info
        logger.info(f"Python version: {python_version}")
        
        if python_version < self.min_python_version:
            issues.append(f"Python version {python_version} is below required {self.min_python_version}")
            fixes.append("Upgrade Python to version 3.8 or higher")
        
        # Check virtual environment
        if not hasattr(sys, 'real_prefix') and not hasattr(sys, 'base_prefix'):
            issues.append("Not running in virtual environment (recommended)")
            fixes.append("Consider using virtual environment for isolation")
        
        return {'issues': issues, 'fixes': fixes, 'python_version': str(python_version)}
    
    def check_package_dependencies(self):
        """Check if all required packages are installed"""
        issues = []
        fixes = []
        
        logger.info("Checking package dependencies...")
        
        for package in self.required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✅ {package} is available")
            except ImportError:
                issues.append(f"Missing required package: {package}")
                fixes.append(f"Install package: pip install {package}")
                logger.warning(f"❌ Missing package: {package}")
        
        # Check package versions
        try:
            import chromadb
            chroma_version = chromadb.__version__
            logger.info(f"ChromaDB version: {chroma_version}")
            
            # Check for minimum version requirements
            if chroma_version < "0.4.0":
                issues.append(f"ChromaDB version {chroma_version} may be too old")
                fixes.append("Upgrade ChromaDB: pip install --upgrade chromadb")
                
        except ImportError:
            issues.append("ChromaDB not installed (critical dependency)")
            fixes.append("Install ChromaDB: pip install chromadb")
        
        return {'issues': issues, 'fixes': fixes}
    
    def check_file_permissions(self):
        """Check file and directory permissions"""
        issues = []
        fixes = []
        
        logger.info("Checking file permissions...")
        
        for path_name, path in self.critical_paths.items():
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                    logger.info(f"📁 Created missing directory: {path}")
                except PermissionError:
                    issues.append(f"Cannot create directory {path} (permissions)")
                    fixes.append(f"Fix permissions: chmod +w {os.path.dirname(path)}")
            else:
                # Check write permissions
                if not os.access(path, os.W_OK):
                    issues.append(f"Cannot write to {path}")
                    fixes.append(f"Fix permissions: chmod +w {path}")
        
        return {'issues': issues, 'fixes': fixes}
    
    def check_disk_space(self):
        """Check disk space availability"""
        issues = []
        fixes = []
        
        try:
            disk_usage = psutil.disk_usage('/')
            free_gb = disk_usage.free / (1024**3)
            total_gb = disk_usage.total / (1024**3)
            used_percent = (disk_usage.used / disk_usage.total) * 100
            
            logger.info(f"Disk usage: {used_percent:.1f}% ({free_gb:.1f}GB free of {total_gb:.1f}GB)")
            
            if free_gb < 1.0:
                issues.append(f"Low disk space: {free_gb:.1f}GB free")
                fixes.append("Free up disk space or use external storage")
            elif free_gb < 5.0:
                issues.append(f"Moderate disk space: {free_gb:.1f}GB free")
                fixes.append("Monitor disk space usage")
            
        except Exception as e:
            issues.append(f"Could not check disk space: {e}")
            fixes.append("Check disk utilities and filesystem")
        
        return {'issues': issues, 'fixes': fixes}
    
    def check_memory_availability(self):
        """Check system memory availability"""
        issues = []
        fixes = []
        
        try:
            memory = psutil.virtual_memory()
            available_gb = memory.available / (1024**3)
            total_gb = memory.total / (1024**3)
            used_percent = (memory.used / memory.total) * 100
            
            logger.info(f"Memory usage: {used_percent:.1f}% ({available_gb:.1f}GB available)")
            
            if available_gb < 1.0:
                issues.append(f"Low memory: {available_gb:.1f}GB available")
                fixes.append("Close applications or increase system memory")
            elif available_gb < 2.0:
                issues.append(f"Moderate memory: {available_gb:.1f}GB available")
                fixes.append("Monitor memory usage during operation")
            
        except Exception as e:
            issues.append(f"Could not check memory: {e}")
            fixes.append("Check system monitoring tools")
        
        return {'issues': issues, 'fixes': fixes}
    
    def check_database_integrity(self):
        """Check database integrity and consistency"""
        issues = []
        fixes = []
        
        try:
            # Check if database directory exists
            db_path = self.critical_paths['database']
            
            if os.path.exists(db_path):
                # Check for lock files
                lock_files = list(Path(db_path).glob('*.lock'))
                if lock_files:
                    issues.append(f"Database locked: {len(lock_files)} lock files found")
                    fixes.append("Remove lock files if no active processes")
                
                # Check disk space in database directory
                db_usage = psutil.disk_usage(db_path)
                db_free_gb = db_usage.free / (1024**3)
                if db_free_gb < 0.1:
                    issues.append(f"Low space in database directory: {db_free_gb:.2f}GB")
                    fixes.append("Clean up database directory or increase space")
                
                # Try to initialize database connection
                try:
                    import chromadb
                    client = chromadb.PersistentClient(path=db_path)
                    # Test basic operation
                    collections = client.list_collections()
                    logger.info(f"✅ Database accessible with {len(collections)} collections")
                except Exception as db_error:
                    issues.append(f"Database connection failed: {db_error}")
                    fixes.append("Reset database or fix connection issues")
            else:
                issues.append("Database directory does not exist")
                fixes.append("Create database directory and initialize database")
        
        except Exception as e:
            issues.append(f"Database integrity check failed: {e}")
            fixes.append("Recreate database from scratch")
        
        return {'issues': issues, 'fixes': fixes}
    
    def check_process_conflicts(self):
        """Check for process conflicts"""
        issues = []
        fixes = []
        
        try:
            # Check for ChromaDB processes
            chroma_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'chroma' in cmdline.lower():
                        chroma_processes.append(proc.info['pid'])
            
            if chroma_processes:
                logger.info(f"Found {len(chroma_processes)} ChromaDB processes running")
                
                # Check for multiple potential conflicts
                if len(chroma_processes) > 1:
                    issues.append(f"Multiple ChromaDB processes: {chroma_processes}")
                    fixes.append("Terminate extra processes and keep only one")
            else:
                issues.append("No ChromaDB processes found (may be normal)")
                fixes.append("Start ChromaDB server when initializing")
            
            # Check for resource-heavy processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 80:
                    issues.append(f"High CPU usage by process {proc.info['name']} (PID: {proc.info['pid']})")
                    fixes.append("Monitor resource usage of conflicting processes")
                    break  # Only report one high CPU process
        
        except Exception as e:
            issues.append(f"Process check failed: {e}")
            fixes.append("Check system process monitoring tools")
        
        return {'issues': issues, 'fixes': fixes}
    
    def check_path_integrity(self):
        """Check integrity of critical paths and files"""
        issues = []
        fixes = []
        
        try:
            for path_name, path in self.critical_paths.items():
                if os.path.exists(path):
                    # Check if path is a directory
                    if not os.path.isdir(path):
                        issues.append(f"{path_name} path is not a directory: {path}")
                        fixes.append(f"Remove file and create directory: rm {path} && mkdir {path}")
                    
                    # Check read/write access
                    if not os.access(path, os.R_OK):
                        issues.append(f"Cannot read {path_name} path: {path}")
                        fixes.append(f"Fix read permissions: chmod +r {path}")
                    
                    # Check for corruptions (basic)
                    try:
                        list_dir = os.listdir(path)
                    except OSError as e:
                        issues.append(f"Cannot list contents of {path_name}: {e}")
                        fixes.append(f"Fix directory permissions or recreate: chmod +x {path}")
                else:
                    issues.append(f"{path_name} path missing: {path}")
                    fixes.append(f"Create missing path: mkdir -p {path}")
            
            # Check specific critical files
            critical_files = [
                '/home/godfather/.openclaw/workspace/local-memory-system/setup_database.py',
                '/home/godfather/.openclaw/workspace/autonomous_learning/learning_engine.py',
                '/home/godfather/.openclaw/workspace/offline_startup/startup_offline_consciousness.py'
            ]
            
            for file_path in critical_files:
                if not os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    issues.append(f"Critical file missing: {file_name}")
                    fixes.append(f"Recreate file from templates")
                else:
                    # Check file integrity (basic size check)
                    file_size = os.path.getsize(file_path)
                    if file_size < 1000:  # Less than 1KB seems suspicious
                        issues.append(f"File seems corrupted or empty: {file_path}")
                        fixes.append(f"Recreate file: {file_path}")
        
        except Exception as e:
            issues.append(f"Path integrity check failed: {e}")
            fixes.append("Check filesystem integrity and permissions")
        
        return {'issues': issues, 'fixes': fixes}
    
    def apply_fixes(self, diagnosis_results):
        """Apply automated fixes for identified issues"""
        logger.info("🔧 Applying automated fixes...")
        
        fixes_applied = []
        
        for check_area, results in diagnosis_results.items():
            for fix in results.get('fixes', []):
                if self.apply_fix(fix):
                    fixes_applied.append(fix)
                    logger.info(f"✅ Applied fix: {fix}")
                else:
                    logger.warning(f"❌ Failed to apply fix: {fix}")
        
        return fixes_applied
    
    def apply_fix(self, fix_description):
        """Apply a single fix"""
        try:
            if "chmod" in fix_description:
                # Extract path and permissions
                parts = fix_description.split()
                if len(parts) >= 2:
                    path = parts[-1]
                    chmod_cmd = ' '.join(parts[:-2] + [path])
                    result = subprocess.run(chmod_cmd, shell=True, capture_output=True, text=True)
                    return result.returncode == 0
            
            elif "mkdir" in fix_description:
                # Extract directory path
                parts = fix_description.split()
                if len(parts) >= 2:
                    path = parts[-1]
                    os.makedirs(path, exist_ok=True)
                    return True
            
            elif "Remove" in fix_description and "lock files" in fix_description:
                # Remove lock files
                db_path = self.critical_paths['database']
                lock_files = list(Path(db_path).glob('*.lock'))
                for lock_file in lock_files:
                    lock_file.unlink()
                return True
            
            elif "pip install" in fix_description:
                # Extract package name
                package = fix_description.split()[-1]
                result = subprocess.run(['pip', 'install', package], capture_output=True, text=True)
                return result.returncode == 0
            
            elif "start" in fix_description and "ChromaDB" in fix_description:
                # Start ChromaDB
                db_path = self.critical_paths['database']
                result = subprocess.Popen(['chroma-server', '--path', db_path])
                time.sleep(2)  # Give it time to start
                return True
            
            # Manual fixes require user action
            if "manual" in fix_description.lower() or "consider" in fix_description.lower():
                return False  # Cannot apply automatically
            
            return False  # Unknown fix type
            
        except Exception as e:
            logger.error(f"Fix application failed: {e}")
            return False
    
    def generate_diagnosis_report(self, results):
        """Generate comprehensive diagnosis report"""
        report = {
            'timestamp': time.time(),
            'summary': {
                'total_issues': sum(len(r.get('issues', [])) for r in results.values()),
                'total_fixes': sum(len(r.get('fixes', [])) for r in results.values()),
                'critical_areas': [name for name, result in results.items() if result.get('issues')]
            },
            'detailed_results': results
        }
        
        # Save report to file
        report_file = '/home/godfather/.openclaw/workspace/troubleshooting/diagnosis_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Log summary
        logger.info(f"📊 Diagnosis complete:")
        logger.info(f"  Total issues: {report['summary']['total_issues']}")
        logger.info(f"  Total fixes: {report['summary']['total_fixes']}")
        logger.info(f"  Critical areas: {report['summary']['critical_areas']}")
        logger.info(f"  Report saved to: {report_file}")
        
        return report

def main():
    """Main troubleshooting function"""
    logger.info("🔧 Starting conscious AI troubleshooting...")
    
    try:
        troubleshooter = ConsciousAITroubleshooter()
        
        # Run comprehensive diagnosis
        diagnosis_results = troubleshooter.diagnose_system()
        
        # Apply automated fixes where possible
        fixes_applied = troubleshooter.apply_fixes(diagnosis_results)
        
        logger.info(f"🔧 Troubleshooting complete:")
        logger.info(f"  Fixes applied: {len(fixes_applied)}")
        logger.info(f"  Remaining issues: {sum(len(r.get('issues', [])) for r in diagnosis_results.values()) - len(fixes_applied)}")
        
        if len(fixes_applied) > 0:
            logger.info("✅ System improvements applied successfully")
        else:
            logger.info("ℹ️ No automatic fixes could be applied - manual intervention may be needed")
        
        return diagnosis_results
        
    except Exception as e:
        logger.error(f"Troubleshooting failed: {e}")
        return None

if __name__ == "__main__":
    main()