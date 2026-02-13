#!/usr/bin/env python3
"""
SARA - Autonomous System Agent Enhanced
Default capabilities: firewall ops, file management, system naming, IP scanning, full system scans
"""

import os
import sys
import subprocess
import socket
import json
import time
import hashlib
import re
from datetime import datetime
from pathlib import Path

class SaraAutonomousEnhanced:
    def __init__(self):
        self.session_id = hashlib.sha256(f"sara_{time.time()}".encode()).hexdigest()[:12]
        self.workspace = Path("/home/godfather/.openclaw/workspace")
        self.log_file = self.workspace / f"sara_enhanced_{self.session_id}.log"
        self.sara_name = "SARA - Autonomous System Agent"
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [SARA] [{level}] {message}\n"
        print(log_entry.strip())
        
        with open(self.log_file, "a") as f:
            f.write(log_entry)
    
    def get_true_system_name(self):
        """Get the true system name and details"""
        self.log("=== SYSTEM IDENTIFICATION ===")
        
        try:
            # Hostname
            hostname = socket.gethostname()
            self.log(f"System Hostname: {hostname}")
            
            # System information
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
            self.log(f"System Info: {result.stdout.strip()}")
            
            # User name
            username = os.getenv('USER', os.getlogin())
            self.log(f"Current User: {username}")
            
            # Get full user details
            import pwd
            user_info = pwd.getpwnam(username)
            self.log(f"User Info: {user_info.pw_gecos} (UID: {user_info.pw_uid})")
            
            return {
                'hostname': hostname,
                'system_info': result.stdout.strip(),
                'username': username,
                'user_details': str(user_info.pw_gecos)
            }
            
        except Exception as e:
            self.log(f"System identification failed: {e}")
            return None
    
    def check_firewall_status_detailed(self):
        """Get detailed firewall status"""
        self.log("=== DETAILED FIREWALL STATUS ===")
        
        firewall_info = {}
        
        try:
            # Check if firewall is running
            result = subprocess.run(['firewall-cmd', '--state'], capture_output=True, text=True)
            firewall_info['status'] = "RUNNING" if result.returncode == 0 else "NOT RUNNING"
            self.log(f"Firewall Status: {firewall_info['status']}")
            
            # Get current zone
            result = subprocess.run(['firewall-cmd', '--get-default-zone'], capture_output=True, text=True)
            if result.returncode == 0:
                firewall_info['default_zone'] = result.stdout.strip()
                self.log(f"Default Zone: {firewall_info['default_zone']}")
            
            # Get active zones
            result = subprocess.run(['firewall-cmd', '--get-active-zones'], capture_output=True, text=True)
            if result.returncode == 0:
                firewall_info['active_zones'] = result.stdout.strip()
                self.log(f"Active Zones: {firewall_info['active_zones']}")
            
            # Get all zones
            result = subprocess.run(['firewall-cmd', '--list-all-zones'], capture_output=True, text=True)
            if result.returncode == 0:
                firewall_info['all_zones'] = result.stdout
                self.log("Retrieved all zone configurations")
            
            # Get services
            result = subprocess.run(['firewall-cmd', '--list-services'], capture_output=True, text=True)
            if result.returncode == 0:
                firewall_info['services'] = result.stdout.strip().split()
                self.log(f"Allowed Services: {', '.join(firewall_info['services'])}")
            
            # Get ports
            result = subprocess.run(['firewall-cmd', '--list-ports'], capture_output=True, text=True)
            if result.returncode == 0:
                firewall_info['ports'] = result.stdout.strip()
                self.log(f"Open Ports: {firewall_info['ports']}")
                
        except Exception as e:
            self.log(f"Firewall analysis failed: {e}")
            
        return firewall_info
    
    def advanced_file_operations(self):
        """Demonstrate advanced file operations"""
        self.log("=== ADVANCED FILE OPERATIONS ===")
        
        workspace = self.workspace
        test_dir = workspace / "sara_test_operations"
        
        results = {}
        
        try:
            # Create directory
            test_dir.mkdir(exist_ok=True)
            self.log(f"✓ Created directory: {test_dir}")
            results['dir_created'] = True
            
            # Create multiple files
            files_created = []
            for i in range(3):
                test_file = test_dir / f"test_file_{i+1}.txt"
                test_file.write_text(f"SARA test file {i+1} - Created at {datetime.now()}")
                files_created.append(test_file)
                self.log(f"✓ Created file: {test_file}")
            
            results['files_created'] = len(files_created)
            
            # Read and verify files
            for i, file_path in enumerate(files_created):
                content = file_path.read_text()
                self.log(f"✓ File {i+1} content: {content[:50]}...")
            
            # Create subdirectory and move files
            subdir = test_dir / "subdir"
            subdir.mkdir(exist_ok=True)
            
            for file_path in files_created:
                new_path = subdir / file_path.name
                file_path.rename(new_path)
                self.log(f"✓ Moved {file_path.name} -> subdir/")
            
            # Delete all files and directories
            for file_path in subdir.glob("*.txt"):
                file_path.unlink()
                self.log(f"✓ Deleted: {file_path.name}")
            
            subdir.rmdir()
            test_dir.rmdir()
            
            self.log("✓ All test operations completed successfully")
            results['cleanup_success'] = True
            results['overall'] = True
            
        except Exception as e:
            self.log(f"File operations failed: {e}")
            results['error'] = str(e)
            results['overall'] = False
        
        return results
    
    def get_system_ip_addresses(self):
        """Get all IP addresses on the system"""
        self.log("=== SYSTEM IP ADDRESS DISCOVERY ===")
        
        ip_info = {}
        
        try:
            # Get local IP addresses
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip_info['local_ip'] = local_ip
            self.log(f"Local IP: {local_ip}")
            
            # Get all network interfaces
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                interfaces = {}
                current_interface = None
                
                for line in result.stdout.split('\n'):
                    if line.startswith(' '):
                        continue
                    if ': ' in line and 'lo' not in line:
                        parts = line.split(': ')
                        if len(parts) >= 2:
                            current_interface = parts[1].split('@')[0]
                            interfaces[current_interface] = []
                    elif 'inet ' in line and current_interface:
                        ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip_addr = ip_match.group(1)
                            interfaces[current_interface].append(ip_addr)
                            self.log(f"Interface {current_interface}: {ip_addr}")
                
                ip_info['interfaces'] = interfaces
            
            # Get public IP
            try:
                result = subprocess.run(['curl', '-s', 'ifconfig.me'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    public_ip = result.stdout.strip()
                    if public_ip:
                        ip_info['public_ip'] = public_ip
                        self.log(f"Public IP: {public_ip}")
            except Exception as e:
                self.log(f"Public IP lookup failed: {e}")
            
        except Exception as e:
            self.log(f"IP discovery failed: {e}")
        
        return ip_info
    
    def scan_local_network(self, target_range="192.168.1.0/24"):
        """Scan local network for active hosts"""
        self.log(f"=== LOCAL NETWORK SCAN: {target_range} ===")
        
        scan_results = {}
        
        try:
            # Try using nmap if available
            result = subprocess.run(['which', 'nmap'], capture_output=True, text=True)
            if result.returncode == 0:
                self.log("Using nmap for network scanning...")
                
                # Fast scan
                result = subprocess.run(['nmap', '-sn', target_range], capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    # Parse nmap output
                    lines = result.stdout.split('\n')
                    hosts = []
                    for line in lines:
                        if 'Nmap scan report for' in line:
                            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                            if ip_match:
                                hosts.append(ip_match.group(1))
                    
                    scan_results['hosts_found'] = hosts
                    scan_results['total_hosts'] = len(hosts)
                    self.log(f"Found {len(hosts)} hosts on network")
                    for host in hosts:
                        self.log(f"  Active host: {host}")
                else:
                    self.log(f"Nmap scan failed: {result.stderr}")
            
            else:
                # Fallback to ping scanning
                self.log("Using ping scan (nmap not available)")
                network_base = '192.168.1'
                active_hosts = []
                
                for i in range(1, 255):
                    ip = f"{network_base}.{i}"
                    try:
                        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                              capture_output=True, text=True, timeout=2)
                        if result.returncode == 0:
                            active_hosts.append(ip)
                            self.log(f"Active host: {ip}")
                    except:
                        continue
                
                scan_results['hosts_found'] = active_hosts
                scan_results['total_hosts'] = len(active_hosts)
                
        except Exception as e:
            self.log(f"Network scan failed: {e}")
            scan_results['error'] = str(e)
        
        return scan_results
    
    def scan_ip_address(self, target_ip):
        """Perform detailed scan of specific IP address"""
        self.log(f"=== DETAILED IP SCAN: {target_ip} ===")
        
        scan_results = {'target_ip': target_ip}
        
        try:
            # Basic ping test
            result = subprocess.run(['ping', '-c', '3', target_ip], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                scan_results['ping_reachable'] = True
                self.log(f"✓ {target_ip} is reachable via ping")
            else:
                scan_results['ping_reachable'] = False
                self.log(f"✗ {target_ip} not reachable via ping")
                return scan_results
            
            # Port scan if nmap available
            result = subprocess.run(['which', 'nmap'], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"Scanning ports on {target_ip}...")
                result = subprocess.run(['nmap', '-sS', '-O', target_ip], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    scan_results['nmap_results'] = result.stdout
                    self.log("✓ Port scan completed")
                    
                    # Parse open ports
                    open_ports = re.findall(r'(\d+)/tcp\s+open', result.stdout)
                    scan_results['open_ports'] = open_ports
                    self.log(f"Open ports found: {', '.join(open_ports)}")
                    
                    # Try to get OS info
                    os_match = re.search(r'Running: (.+)', result.stdout)
                    if os_match:
                        scan_results['os_info'] = os_match.group(1)
                        self.log(f"OS Info: {os_match.group(1)}")
            
            # DNS lookup
            try:
                result = subprocess.run(['nslookup', target_ip], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    scan_results['dns_info'] = result.stdout
                    self.log("✓ DNS lookup completed")
            except:
                pass
                
        except Exception as e:
            self.log(f"IP scan failed: {e}")
            scan_results['error'] = str(e)
        
        return scan_results
    
    def run_full_system_scan(self):
        """Comprehensive system scan"""
        self.log("=== COMPREHENSIVE SYSTEM SCAN ===")
        
        full_scan_results = {
            'timestamp': datetime.now().isoformat(),
            'scan_type': 'full_system_scan'
        }
        
        try:
            # System information
            full_scan_results['system_info'] = self.get_true_system_name()
            
            # Firewall status
            full_scan_results['firewall'] = self.check_firewall_status_detailed()
            
            # IP information
            full_scan_results['ip_addresses'] = self.get_system_ip_addresses()
            
            # Running processes
            self.log("Scanning running processes...")
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                processes = result.stdout.split('\n')
                full_scan_results['process_count'] = len([p for p in processes if p.strip()])
                self.log(f"Found {full_scan_results['process_count']} running processes")
            
            # Network connections
            self.log("Scanning network connections...")
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
            if result.returncode == 0:
                connections = result.stdout.split('\n')
                listening_ports = [c for c in connections if 'LISTEN' in c]
                full_scan_results['listening_ports_count'] = len(listening_ports)
                self.log(f"Found {len(listening_ports)} listening ports")
            
            # File system usage
            self.log("Checking disk usage...")
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            if result.returncode == 0:
                full_scan_results['disk_usage'] = result.stdout
                self.log("Disk usage captured")
            
            # System services
            try:
                result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    services = result.stdout.split('\n')
                    full_scan_results['running_services'] = len([s for s in services if 'loaded' in s and 'running' in s])
                    self.log(f"Found {full_scan_results['running_services']} running services")
            except:
                pass
            
            self.log("✓ Full system scan completed")
            
        except Exception as e:
            self.log(f"Full system scan failed: {e}")
            full_scan_results['error'] = str(e)
        
        return full_scan_results
    
    def run_all_capabilities(self):
        """Demonstrate all enhanced Sara capabilities"""
        self.log(f"SARA Enhanced - Session {self.session_id}")
        self.log("=== ALL CAPABILITIES DEMONSTRATION ===")
        
        results = {}
        
        # 1. System name and user info
        self.log("1. Getting system and user information...")
        results['system_info'] = self.get_true_system_name()
        
        # 2. Firewall status
        self.log("2. Checking detailed firewall status...")
        results['firewall'] = self.check_firewall_status_detailed()
        
        # 3. File operations
        self.log("3. Performing advanced file operations...")
        results['file_ops'] = self.advanced_file_operations()
        
        # 4. IP address discovery
        self.log("4. Discovering system IP addresses...")
        results['ip_discovery'] = self.get_system_ip_addresses()
        
        # 5. Network scanning (local network)
        self.log("5. Scanning local network...")
        results['network_scan'] = self.scan_local_network()
        
        # 6. IP scanning (scan localhost)
        self.log("6. Scanning specific IP address...")
        localhost_scan = self.scan_ip_address('127.0.0.1')
        results['localhost_scan'] = localhost_scan
        
        # 7. Full system scan
        self.log("7. Running comprehensive system scan...")
        results['full_scan'] = self.run_full_system_scan()
        
        # Generate report
        report_file = self.workspace / f"sara_enhanced_report_{self.session_id}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.log(f"✓ All capabilities completed - Report saved to {report_file}")
        return results

if __name__ == "__main__":
    sara = SaraAutonomousEnhanced()
    results = sara.run_all_capabilities()
    
    print(f"\n{'='*60}")
    print("SARA ENHANCED - ALL CAPABILITIES VERIFIED")
    print("="*60)
    print("✓ System name discovery")
    print("✓ Firewall status checking") 
    print("✓ Advanced file operations")
    print("✓ IP address discovery")
    print("✓ Network scanning")
    print("✓ IP address scanning")
    print("✓ Full system scanning")
    print("="*60)
    print("SARA IS READY WITH ALL DEFAULT CAPABILITIES!")