#!/usr/bin/env python3
"""
PostHog Pi - Development Server
Quick way to run the integrated application
"""

import subprocess
import sys
import os

def build_frontend():
    """Build React frontend"""
    print("Building React frontend...")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Install npm dependencies
    subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
    
    # Build React app
    subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True)
    print("Frontend build complete!")

def run_server():
    """Run the Flask server"""
    print("Starting integrated Flask server...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Run the Flask app
    sys.path.append(backend_dir)
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    try:
        build_frontend()
        run_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)