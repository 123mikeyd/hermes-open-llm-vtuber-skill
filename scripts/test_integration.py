#!/usr/bin/env python3
"""
Test script for Open-LLM-VTuber + Hermes Agent integration
This script tests the connection between Open-LLM-VTuber and Hermes Agent
"""

import asyncio
import websockets
import json
import requests
import time
import sys
from typing import Optional, Dict, Any

class IntegrationTester:
    def __init__(self, hermes_url: str = "http://localhost:8000", vtuber_url: str = "ws://localhost:3000"):
        self.hermes_url = hermes_url
        self.vtuber_url = vtuber_url
        self.test_results = []
    
    def test_hermes_connection(self) -> bool:
        """Test connection to Hermes Agent API"""
        print("Testing Hermes Agent connection...")
        try:
            response = requests.get(f"{self.hermes_url}/v1/models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Connected to Hermes Agent")
                print(f"  Available models: {data.get('data', [])}")
                return True
            else:
                print(f"✗ Hermes Agent returned status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to Hermes Agent")
            print(f"  Make sure Hermes is running on {self.hermes_url}")
            print("  Start with: hermes --api-port 8000 --api-mode openai")
            return False
        except Exception as e:
            print(f"✗ Error testing Hermes connection: {e}")
            return False
    
    def test_hermes_chat(self, message: str = "Hello, how are you?") -> bool:
        """Test chat completion with Hermes Agent"""
        print(f"\nTesting Hermes chat with message: '{message}'")
        try:
            payload = {
                "model": "hermes-agent",
                "messages": [
                    {"role": "user", "content": message}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.hermes_url}/v1/chat/completions",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"✓ Received response: {content[:100]}...")
                return True
            else:
                print(f"✗ Chat request failed with status: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Error testing chat: {e}")
            return False
    
    async def test_websocket_connection(self) -> bool:
        """Test WebSocket connection to Open-LLM-VTuber"""
        print(f"\nTesting WebSocket connection to {self.vtuber_url}...")
        try:
            async with websockets.connect(self.vtuber_url, timeout=5) as websocket:
                print("✓ Connected to Open-LLM-VTuber WebSocket")
                
                # Send a test message
                test_message = {
                    "type": "text",
                    "content": "Hello, this is a test message",
                    "timestamp": time.time()
                }
                await websocket.send(json.dumps(test_message))
                print("✓ Sent test message")
                
                # Wait for response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(response)
                    print(f"✓ Received response: {data.get('type', 'unknown')}")
                    return True
                except asyncio.TimeoutError:
                    print("⚠ No response received within 10 seconds")
                    return False
        except websockets.exceptions.ConnectionClosed:
            print("✗ WebSocket connection closed unexpectedly")
            return False
        except websockets.exceptions.InvalidStatusCode as e:
            print(f"✗ WebSocket connection failed: {e}")
            return False
        except Exception as e:
            print(f"✗ Error testing WebSocket: {e}")
            print(f"  Make sure Open-LLM-VTuber is running on {self.vtuber_url}")
            return False
    
    def test_configuration(self, config_path: str = "conf.yaml") -> bool:
        """Test configuration file"""
        print(f"\nTesting configuration file: {config_path}")
        try:
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check required sections
            required_sections = ['system_config', 'character_config']
            for section in required_sections:
                if section not in config:
                    print(f"✗ Missing required section: {section}")
                    return False
            
            # Check LLM configuration
            system_config = config.get('system_config', {})
            if system_config.get('llm_backend') != 'openai':
                print("⚠ LLM backend is not set to 'openai'")
                print("  This integration requires OpenAI-compatible API")
            
            # Check OpenAI configuration
            openai_config = system_config.get('openai', {})
            base_url = openai_config.get('base_url', '')
            if 'localhost:8000' not in base_url:
                print(f"⚠ OpenAI base_url may not point to Hermes: {base_url}")
            
            print("✓ Configuration file looks good")
            return True
        except FileNotFoundError:
            print(f"✗ Configuration file not found: {config_path}")
            return False
        except Exception as e:
            print(f"✗ Error reading configuration: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 60)
        print("Open-LLM-VTuber + Hermes Agent Integration Test")
        print("=" * 60)
        
        tests = [
            ("Hermes Connection", self.test_hermes_connection),
            ("Hermes Chat", lambda: self.test_hermes_chat()),
            ("WebSocket Connection", self.test_websocket_connection),
            ("Configuration", self.test_configuration),
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n{'='*40}")
            print(f"Running: {test_name}")
            print(f"{'='*40}")
            
            try:
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()
                results[test_name] = result
            except Exception as e:
                print(f"✗ Test failed with exception: {e}")
                results[test_name] = False
        
        # Summary
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{test_name:25} {status}")
        
        print(f"\nResult: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! Integration is working correctly.")
            print("\nNext steps:")
            print("1. Start Open-LLM-VTuber: python run_server.py")
            print("2. Open http://localhost:3000 in your browser")
            print("3. Start talking to your AI companion!")
        else:
            print("\n⚠ Some tests failed. Please check the errors above.")
            print("\nTroubleshooting tips:")
            print("1. Ensure Hermes Agent is running: hermes --api-port 8000")
            print("2. Ensure Open-LLM-VTuber is running: python run_server.py")
            print("3. Check configuration in conf.yaml")
            print("4. Verify no port conflicts")
        
        return passed == total

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Open-LLM-VTuber + Hermes integration")
    parser.add_argument("--hermes-url", default="http://localhost:8000", help="Hermes Agent URL")
    parser.add_argument("--vtuber-url", default="ws://localhost:3000", help="Open-LLM-VTuber WebSocket URL")
    parser.add_argument("--config", default="conf.yaml", help="Configuration file path")
    
    args = parser.parse_args()
    
    tester = IntegrationTester(args.hermes_url, args.vtuber_url)
    success = await tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
