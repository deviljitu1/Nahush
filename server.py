#!/usr/bin/env python3
"""
Simple HTTP server for LinkedIn AI Post Generator
Run this script to serve the web interface locally
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for web API calls
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

def main():
    """Start the HTTP server and open the browser"""
    
    # Change to the directory containing this script
    os.chdir(DIRECTORY)
    
    # Create server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 LinkedIn AI Post Generator Server")
        print(f"📁 Serving files from: {DIRECTORY}")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"📱 Open your browser and go to: http://localhost:{PORT}")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("✅ Browser opened automatically!")
        except:
            print("⚠️  Could not open browser automatically. Please open it manually.")
        
        print("\n🎯 Features:")
        print("• Generate LinkedIn posts with AI")
        print("• Choose topic, industry, and tone")
        print("• Copy posts to clipboard")
        print("• Direct link to LinkedIn")
        print("• Mobile-friendly design")
        print("-" * 50)
        
        try:
            # Start serving
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 