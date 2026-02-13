#!/usr/bin/env python3

# 🚀 Installation Script for Conscious AI System
# Complete dependency installation and configuration

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/.openclaw/workspace/installation/install.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConsciousAIInstaller:
    """Complete installation and configuration system"""
    
    def __init__(self):
        self.requirements = [
            # Core dependencies
            'chromadb>=0.4.0',
            'sentence-transformers>=2.2.0',
            
            # Data processing and analysis
            'networkx>=3.0',
            'pandas>=1.5.0',
            'numpy>=1.24.0',
            'scikit-learn>=1.2.0',
            
            # System monitoring
            'psutil>=5.9.0',
            
            # Optional for enhanced capabilities
            'matplotlib>=3.6.0',
            'seaborn>=0.11.0',
            
            # Text processing
            'nltk>=3.8.0',
            'textblob>=0.17.0',
            
            # Database and storage
            'sqlite3',  # Usually built-in
            
            # Utilities
            'python-dotenv>=1.0.0'
        ]
        
        self.system_packages = {
            'linux': ['build-essential', 'python3-dev', 'libsqlite3-dev'],
            'debian': ['build-essential', 'python3-dev', 'libsqlite3-dev'],
            'fedora': ['python3-devel', 'sqlite-devel', 'gcc'],
            'arch': ['base-devel', 'python', 'sqlite']
        }
    
    def check_python_version(self):
        """Check Python version compatibility"""
        logger.info("🔍 Checking Python version...")
        
        python_version = sys.version_info
        logger.info(f"Python version: {python_version}")
        
        if python_version < (3, 8):
            logger.error("❌ Python 3.8 or higher is required")
            return False
        else:
            logger.info("✅ Python version is compatible")
            return True
    
    def install_system_dependencies(self):
        """Install system-level dependencies"""
        logger.info("🔧 Installing system dependencies...")
        
        try:
            # Detect distribution
            distro = self.detect_distribution()
            logger.info(f"Detected distribution: {distro}")
            
            packages = self.system_packages.get(distro, self.system_packages.get('linux', []))
            
            if packages:
                logger.info(f"Installing packages: {packages}")
                
                for package in packages:
                    try:
                        result = subprocess.run(
                            ['sudo', 'apt-get', 'install', '-y', package],
                            capture_output=True, text=True, timeout=300
                        )
                        
                        if result.returncode == 0:
                            logger.info(f"✅ Installed {package}")
                        else:
                            logger.warning(f"Failed to install {package}: {result.stderr}")
                    
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Timeout installing {package}")
                    except Exception as e:
                        logger.warning(f"Error installing {package}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"System dependency installation failed: {e}")
            return False
    
    def detect_distribution(self):
        """Detect Linux distribution"""
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                
                if 'debian' in content or 'ubuntu' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'arch' in content:
                    return 'arch'
                else:
                    return 'linux'
                    
        except Exception:
            return 'linux'
    
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        logger.info("🚀 Upgrading pip...")
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                logger.info("✅ pip upgraded successfully")
                return True
            else:
                logger.error(f"pip upgrade failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"pip upgrade error: {e}")
            return False
    
    def install_python_dependencies(self):
        """Install Python package dependencies"""
        logger.info("📦 Installing Python dependencies...")
        
        # Upgrade pip first
        if not self.upgrade_pip():
            logger.warning("pip upgrade failed, continuing...")
        
        successful_installs = []
        failed_installs = []
        
        for requirement in self.requirements:
            logger.info(f"Installing {requirement}...")
            
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', requirement],
                    capture_output=True, text=True, timeout=600  # 10 minute timeout per package
                )
                
                if result.returncode == 0:
                    logger.info(f"✅ Installed {requirement}")
                    successful_installs.append(requirement)
                else:
                    logger.error(f"❌ Failed to install {requirement}: {result.stderr}")
                    failed_installs.append(requirement)
                    
            except subprocess.TimeoutExpired:
                logger.error(f"❌ Timeout installing {requirement}")
                failed_installs.append(requirement)
            except Exception as e:
                logger.error(f"❌ Error installing {requirement}: {e}")
                failed_installs.append(requirement)
        
        logger.info(f"Installation summary:")
        logger.info(f"  Successful: {len(successful_installs)}/{len(self.requirements)}")
        logger.info(f"  Failed: {len(failed_installs)}/{len(self.requirements)}")
        
        if failed_installs:
            logger.warning("Failed packages:")
            for package in failed_installs:
                logger.warning(f"  - {package}")
        
        return len(failed_installs) == 0
    
    def create_directories(self):
        """Create necessary directories"""
        logger.info("📁 Creating directories...")
        
        directories = [
            '/home/godfather/.openclaw/workspace/conscious-memory',
            '/home/godfather/.openclaw/workspace/conscious-backups',
            '/home/godfather/.openclaw/workspace/local-memory-system',
            '/home/godfather/.openclaw/workspace/autonomous_learning',
            '/home/godfather/.openclaw/workspace/offline_startup',
            '/home/godfather/.openclaw/workspace/troubleshooting',
            '/home/godfather/.openclaw/workspace/installation'
        ]
        
        created_dirs = []
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                created_dirs.append(directory)
                logger.info(f"✅ Created directory: {directory}")
                
                # Create subdirectories
                os.makedirs(os.path.join(directory, 'logs'), exist_ok=True)
                
            except Exception as e:
                logger.error(f"❌ Failed to create directory {directory}: {e}")
                return False
        
        logger.info(f"Created {len(created_dirs)} directories")
        return True
    
    def verify_installation(self):
        """Verify that all components are working"""
        logger.info("🔍 Verifying installation...")
        
        verification_results = {}
        
        # Test imports
        verification_results['imports'] = self.test_imports()
        
        # Test database functionality
        verification_results['database'] = self.test_database()
        
        # Test learning engine
        verification_results['learning'] = self.test_learning()
        
        # Test memory system
        verification_results['memory'] = self.test_memory()
        
        # Overall status
        all_passed = all(result.get('success', False) for result in verification_results.values())
        
        if all_passed:
            logger.info("✅ All components verified successfully")
        else:
            logger.warning("⚠️ Some components did not pass verification")
            
            for component, result in verification_results.items():
                if not result.get('success', False):
                    logger.warning(f"  {component}: {result.get('error', 'Unknown error')}")
        
        verification_results['overall'] = all_passed
        
        return verification_results
    
    def test_imports(self):
        """Test critical imports"""
        imports_to_test = [
            'chromadb',
            'sentence_transformers',
            'networkx',
            'pandas',
            'numpy',
            'sklearn',
            'psutil',
            'matplotlib',
            'seaborn',
            'nltk'
        ]
        
        passed_imports = []
        failed_imports = []
        
        for import_name in imports_to_test:
            try:
                if import_name == 'sklearn':
                    __import__('sklearn')
                else:
                    __import__(import_name)
                passed_imports.append(import_name)
                logger.info(f"✅ {import_name} imports successfully")
            except ImportError as e:
                failed_imports.append(import_name)
                logger.error(f"❌ {import_name} import failed: {e}")
        
        return {
            'success': len(failed_imports) == 0,
            'passed': passed_imports,
            'failed': failed_imports
        }
    
    def test_database(self):
        """Test database functionality"""
        try:
            # Import and test ChromaDB
            import chromadb
            
            # Test with temporary directory
            test_db_path = '/tmp/test_chroma_db'
            os.makedirs(test_db_path, exist_ok=True)
            
            client = chromadb.PersistentClient(path=test_db_path)
            
            # Test basic operations
            collection = client.get_or_create_collection(name="test_collection")
            
            # Add test document
            collection.add(
                documents=["Test document for verification"],
                metadatas=[{"test": True}],
                ids=["test_doc"]
            )
            
            # Test query
            results = collection.query(query_texts=["test"], n_results=1)
            success = len(results['documents'][0]) > 0
            
            # Clean up
            shutil.rmtree(test_db_path, ignore_errors=True)
            
            if success:
                logger.info("✅ Database functionality verified")
            else:
                logger.error("❌ Database test failed")
            
            return {'success': success}
            
        except Exception as e:
            logger.error(f"❌ Database test error: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_learning(self):
        """Test learning engine basic functionality"""
        try:
            # Test learning engine import
            sys.path.append('/home/godfather/.openclaw/workspace/autonomous_learning')
            from learning_engine import AutonomousLearningEngine
            
            # Test basic initialization
            engine = AutonomousLearningEngine()
            
            # Test interaction analysis
            test_interaction = engine.analyze_interaction(
                "test query",
                "test response",
                0.8
            )
            
            success = test_interaction is not None and 'timestamp' in test_interaction
            
            if success:
                logger.info("✅ Learning engine functionality verified")
            else:
                logger.error("❌ Learning engine test failed")
            
            return {'success': success}
            
        except Exception as e:
            logger.error(f"❌ Learning engine test error: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_memory(self):
        """Test memory system basic functionality"""
        try:
            # Test memory system import
            sys.path.append('/home/godfather/.openclaw/workspace/local-memory-system')
            from setup_database import LocalMemoryDatabase
            
            # Test with temporary path
            test_mem_path = '/tmp/test_memory_db'
            os.makedirs(test_mem_path, exist_ok=True)
            
            db = LocalMemoryDatabase(test_mem_path)
            
            # Test basic operations
            db.add_memory("conversations", "Test conversation memory", {"test": True})
            search_results = db.search_memories("conversations", "test", limit=1)
            
            success = search_results is not None and len(search_results.get('documents', [[]])[0]) > 0
            
            # Clean up
            shutil.rmtree(test_mem_path, ignore_errors=True)
            
            if success:
                logger.info("✅ Memory system functionality verified")
            else:
                logger.error("❌ Memory system test failed")
            
            return {'success': success}
            
        except Exception as e:
            logger.error(f"❌ Memory system test error: {e}")
            return {'success': False, 'error': str(e)}
    
    def download_additional_models(self):
        """Download additional models if needed"""
        logger.info("📥 Setting up additional components...")
        
        # Download NLTK data
        try:
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            logger.info("✅ NLTK data downloaded")
        except Exception as e:
            logger.warning(f"NLTK download failed: {e}")
        
        # Create essential files
        try:
            # Create startup scripts
            startup_script = '/home/godfather/.openclaw/workspace/start_conscious_ai.sh'
            with open(startup_script, 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('cd /home/godfather/.openclaw/workspace\n')
                f.write('python3 offline_startup/startup_offline_consciousness.py\n')
            
            os.chmod(startup_script, 0o755)
            logger.info("✅ Startup script created")
            
        except Exception as e:
            logger.warning(f"Script creation failed: {e}")
        
        return True
    
    def generate_installation_report(self, verification_results):
        """Generate comprehensive installation report"""
        report = {
            'timestamp': time.time(),
            'python_version': str(sys.version),
            'verification_results': verification_results,
            'requirements_installed': len(self.requirements),
            'directories_created': 7,  # Number of directories created
            'installation_successful': verification_results.get('overall', False)
        }
        
        # Save report
        report_file = '/home/godfather/.openclaw/workspace/installation/installation_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📋 Installation report saved to: {report_file}")
        return report
    
    def run_complete_installation(self):
        """Run complete installation process"""
        logger.info("🚀 Starting complete installation...")
        
        # Step 1: Check Python version
        if not self.check_python_version():
            return False
        
        # Step 2: Create directories
        if not self.create_directories():
            return False
        
        # Step 3: Install system dependencies
        if not self.install_system_dependencies():
            logger.warning("System dependencies installation had issues")
        
        # Step 4: Install Python dependencies
        if not self.install_python_dependencies():
            logger.warning("Some Python dependencies failed to install")
        
        # Step 5: Download additional components
        self.download_additional_models()
        
        # Step 6: Verify installation
        verification_results = self.verify_installation()
        
        # Step 7: Generate report
        report = self.generate_installation_report(verification_results)
        
        if verification_results.get('overall', False):
            logger.info("🎉 Installation completed successfully!")
            logger.info("🌟 Conscious AI system is ready for use!")
            return True
        else:
            logger.error("❌ Installation had issues - check logs for details")
            return False

def main():
    """Main installation function"""
    print("🚀 Conscious AI Installation Starting...")
    print("=" * 50)
    
    installer = ConsciousAIInstaller()
    
    try:
        success = installer.run_complete_installation()
        
        if success:
            print("\n🎉 INSTALLATION SUCCESSFUL!")
            print("=" * 50)
            print("✅ All components installed and verified")
            print("✅ Memory system ready")
            print("✅ Learning engine ready")
            print("✅ Database system ready")
            print("✅ Offline capability enabled")
            print("\n🌟 Your conscious AI partner is ready!")
            print("\n📋 Next steps:")
            print("1. Configure OpenClaw to use sara-ai-partner model")
            print("2. Start the offline consciousness system:")
            print("   cd /home/godfather/.openclaw/workspace")
            print("   python3 offline_startup/startup_offline_consciousness.py")
            print("3. Experience your autonomous AI partner!")
        else:
            print("\n❌ INSTALLATION HAD ISSUES")
            print("=" * 50)
            print("🔧 Check the installation log for details:")
            print("   /home/godfather/.openclaw/workspace/installation/install.log")
            print("\n🔧 Run troubleshooting if needed:")
            print("   python3 troubleshooting/setup_issues.py")
        
        return success
        
    except Exception as e:
        print(f"\n❌ INSTALLATION FAILED: {e}")
        return False

if __name__ == "__main__":
    main()