#!/usr/bin/env python3
"""
PostHog Pi - Development Server
Runs Flask with auto-reload and React with file watching
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class DevServer:
    def __init__(self):
        self.frontend_process = None
        self.backend_process = None
        self.project_root = Path(__file__).parent
        
    def start_frontend_watch(self):
        """Start React development build with file watching"""
        print("Starting React development build with file watching...")
        frontend_dir = self.project_root / 'frontend'
        
        # Install dependencies if needed
        if not (frontend_dir / 'node_modules').exists():
            print("Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        
        # Start the dev build process
        self.frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Monitor frontend output in a separate thread
        def monitor_frontend():
            for line in iter(self.frontend_process.stdout.readline, ''):
                print(f"[React] {line.strip()}")
        
        threading.Thread(target=monitor_frontend, daemon=True).start()
        
    def start_backend_dev(self):
        """Start Flask development server with auto-reload"""
        print("Starting Flask development server...")
        backend_dir = self.project_root / 'backend'
        
        # Set up virtual environment if needed
        venv_dir = backend_dir / 'venv'
        if not venv_dir.exists():
            print("Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], cwd=backend_dir, check=True)
        
        # Determine Python and pip paths
        if os.name == 'nt':  # Windows
            python_path = venv_dir / 'Scripts' / 'python.exe'
            pip_path = venv_dir / 'Scripts' / 'pip.exe'
        else:  # Unix-like
            python_path = venv_dir / 'bin' / 'python'
            pip_path = venv_dir / 'bin' / 'pip'
        
        # Install dependencies
        print("Installing Python dependencies...")
        subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'], cwd=backend_dir, check=True)
        
        # Start Flask with debug mode
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'
        
        self.backend_process = subprocess.Popen(
            [str(python_path), 'app.py'],
            cwd=backend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Monitor backend output in a separate thread
        def monitor_backend():
            for line in iter(self.backend_process.stdout.readline, ''):
                print(f"[Flask] {line.strip()}")
        
        threading.Thread(target=monitor_backend, daemon=True).start()
        
    def start(self):
        """Start both frontend and backend development servers"""
        print("🚀 Starting PostHog Pi Development Server")
        print("=" * 50)
        
        try:
            # Start frontend watcher
            self.start_frontend_watch()
            time.sleep(2)  # Give frontend time to start
            
            # Start backend server
            self.start_backend_dev()
            time.sleep(3)  # Give backend time to start
            
            print("\n✅ Development servers started!")
            print("📱 Frontend: Building and watching for changes...")
            print("🔧 Backend: http://localhost:5000 (with auto-reload)")
            print("🌐 Full app: http://localhost:5000")
            print("\nPress Ctrl+C to stop all servers")
            
            # Wait for processes
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("Frontend process stopped")
                    break
                    
                if self.backend_process and self.backend_process.poll() is not None:
                    print("Backend process stopped")
                    break
                    
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """Stop all development servers"""
        print("\n🛑 Stopping development servers...")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                
        print("✅ All servers stopped")

def main():
    """Main entry point"""
    dev_server = DevServer()
    
    # Handle Ctrl+C gracefully
    def signal_handler(signum, frame):
        dev_server.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        dev_server.start()
    except Exception as e:
        print(f"❌ Error: {e}")
        dev_server.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()