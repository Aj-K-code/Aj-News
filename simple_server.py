"""
Simple HTTP server for serving static files for GitHub Pages deployment.
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

class NewsDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # API endpoints
        if path.startswith('/api/'):
            self.handle_api_request(path[5:])  # Remove '/api/' prefix
            return
        
        # Static files
        if path == '/' or path == '/index.html':
            self.path = '/index.html'
        elif path == '/':
            self.path = '/index.html'
            
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def handle_api_request(self, endpoint):
        """Handle API requests with sample data"""
        try:
            if endpoint == 'healthcare':
                data = {
                    "daily_take": "Breakthrough gene therapy shows promising results in early trials for rare childhood disease, while FDA faces pressure to streamline approval processes for life-saving treatments.",
                    "stories": [
                        {
                            "headline": "FDA Announces New Fast-Track Program for Gene Therapies",
                            "summary": "The FDA has unveiled a new expedited review pathway aimed at accelerating the approval of gene therapies for rare diseases, potentially cutting approval times by up to 50%.",
                            "source": "STAT News",
                            "importance": 5,
                            "impact_to_me": 4,
                            "category": "Policy"
                        },
                        {
                            "headline": "Revolutionary CAR-T Cell Therapy Shows 90% Remission Rate",
                            "summary": "A new CAR-T cell therapy targeting pediatric leukemia has demonstrated remarkable efficacy in Phase II trials, with 90% of patients achieving complete remission after six months.",
                            "source": "The Lancet",
                            "importance": 5,
                            "impact_to_me": 5,
                            "category": "Research"
                        },
                        {
                            "headline": "Telehealth Reimbursement Rules Expanded for Rural Areas",
                            "summary": "CMS has expanded Medicare reimbursement for telehealth services in rural communities, removing geographic restrictions that previously limited access to virtual care.",
                            "source": "Fierce Healthcare",
                            "importance": 4,
                            "impact_to_me": 3,
                            "category": "Policy"
                        },
                        {
                            "headline": "AI Diagnostic Tool Achieves Radiologist-Level Accuracy",
                            "summary": "A new artificial intelligence system for detecting lung cancer on CT scans has matched or exceeded the diagnostic accuracy of experienced radiologists in a large clinical trial.",
                            "source": "NEJM",
                            "importance": 4,
                            "impact_to_me": 4,
                            "category": "Tech"
                        },
                        {
                            "headline": "Pharma Giants Merge in $50B Deal to Focus on Rare Diseases",
                            "summary": "Two major pharmaceutical companies have announced a merger valued at $50 billion, creating a new entity that will focus exclusively on developing treatments for ultra-rare genetic disorders.",
                            "source": "Fierce Pharma",
                            "importance": 3,
                            "impact_to_me": 2,
                            "category": "Business"
                        }
                    ]
                }
                self.send_json_response(data)
            elif endpoint == 'general':
                data = {
                    "daily_take": "Major tech companies announce breakthroughs in quantum computing while global markets react to new AI regulations from leading economies.",
                    "stories": [
                        {
                            "headline": "Quantum Supremacy Claimed by Three Major Tech Companies",
                            "summary": "Google, IBM, and a leading Chinese tech firm have simultaneously announced they've achieved quantum supremacy, solving complex problems in minutes that would take traditional supercomputers millennia.",
                            "source": "The Economist",
                            "importance": 5,
                            "impact_to_me": 5,
                            "category": "Technology"
                        },
                        {
                            "headline": "Global AI Regulation Framework Agreed by G7 Nations",
                            "summary": "G7 countries have reached a preliminary agreement on a unified framework for AI governance, establishing new standards for transparency and safety in artificial intelligence development.",
                            "source": "Reuters",
                            "importance": 5,
                            "impact_to_me": 4,
                            "category": "Global"
                        },
                        {
                            "headline": "Renewable Energy Investments Surpass Fossil Fuels for First Time",
                            "summary": "Global investment in renewable energy projects has exceeded fossil fuel investments for the first time in history, signaling a major shift in the energy sector's trajectory.",
                            "source": "BBC",
                            "importance": 4,
                            "impact_to_me": 3,
                            "category": "Business"
                        },
                        {
                            "headline": "Breakthrough in Nuclear Fusion Energy Achieved",
                            "summary": "Scientists at a major research facility have achieved a net energy gain in nuclear fusion, bringing humanity one step closer to unlimited clean energy.",
                            "source": "AP News",
                            "importance": 5,
                            "impact_to_me": 5,
                            "category": "Science"
                        },
                        {
                            "headline": "Global Supply Chain Disruptions Ease as New Routes Established",
                            "summary": "International trade organizations report significant improvements in global supply chain resilience following the establishment of alternative shipping routes and digital logistics platforms.",
                            "source": "WSJ",
                            "importance": 3,
                            "impact_to_me": 3,
                            "category": "Business"
                        }
                    ]
                }
                self.send_json_response(data)
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_server(port=8000):
    """Run the HTTP server"""
    with socketserver.TCPServer(("", port), NewsDashboardHandler) as httpd:
        print(f"Server running at http://localhost:{port}/")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()