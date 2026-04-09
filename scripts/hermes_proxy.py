#!/usr/bin/env python3
"""
WebSocket Proxy for Open-LLM-VTuber + Hermes Agent Integration
This script creates a WebSocket proxy that bridges Open-LLM-VTuber with Hermes Agent
"""

import asyncio
import websockets
import json
import requests
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """Configuration for the proxy"""
    hermes_url: str = "http://localhost:8000"
    proxy_host: str = "localhost"
    proxy_port: int = 8765
    vtuber_backend: str = "ws://localhost:3000"
    max_message_length: int = 1000
    timeout: int = 30

class HermesProxy:
    """Proxy server for Open-LLM-VTuber and Hermes Agent"""
    
    def __init__(self, config: ProxyConfig):
        self.config = config
        self.active_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.conversation_histories: Dict[str, list] = {}
        
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle a WebSocket client connection"""
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"New connection from {client_id}")
        
        self.active_connections[client_id] = websocket
        self.conversation_histories[client_id] = []
        
        try:
            async for message in websocket:
                await self.process_message(client_id, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for {client_id}")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            # Cleanup
            if client_id in self.active_connections:
                del self.active_connections[client_id]
            if client_id in self.conversation_histories:
                del self.conversation_histories[client_id]
    
    async def process_message(self, client_id: str, message: str):
        """Process incoming message from Open-LLM-VTuber"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "text":
                await self.handle_text_message(client_id, data)
            elif message_type == "audio":
                await self.handle_audio_message(client_id, data)
            elif message_type == "control":
                await self.handle_control_message(client_id, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON from {client_id}: {message[:100]}...")
        except Exception as e:
            logger.error(f"Error processing message from {client_id}: {e}")
    
    async def handle_text_message(self, client_id: str, data: Dict[str, Any]):
        """Handle text message by forwarding to Hermes Agent"""
        user_input = data.get("content", "")
        if not user_input:
            return
        
        # Truncate if too long
        if len(user_input) > self.config.max_message_length:
            user_input = user_input[:self.config.max_message_length] + "..."
        
        logger.info(f"Processing text from {client_id}: {user_input[:50]}...")
        
        # Add to conversation history
        if client_id not in self.conversation_histories:
            self.conversation_histories[client_id] = []
        
        self.conversation_histories[client_id].append({
            "role": "user",
            "content": user_input
        })
        
        # Keep history manageable (last 10 messages)
        if len(self.conversation_histories[client_id]) > 20:
            self.conversation_histories[client_id] = self.conversation_histories[client_id][-20:]
        
        try:
            # Call Hermes Agent API
            response = requests.post(
                f"{self.config.hermes_url}/v1/chat/completions",
                json={
                    "model": "hermes-agent",
                    "messages": self.conversation_histories[client_id],
                    "max_tokens": 500,
                    "temperature": 0.7,
                    "stream": False
                },
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result["choices"][0]["message"]["content"]
                
                # Add to history
                self.conversation_histories[client_id].append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Send response back to client
                websocket = self.active_connections.get(client_id)
                if websocket:
                    response_data = {
                        "type": "text",
                        "content": assistant_message,
                        "timestamp": datetime.now().isoformat(),
                        "emotion": self.detect_emotion(assistant_message)
                    }
                    await websocket.send(json.dumps(response_data))
                    logger.info(f"Sent response to {client_id}: {assistant_message[:50]}...")
            else:
                logger.error(f"Hermes API error: {response.status_code} - {response.text}")
                await self.send_error(client_id, "Failed to get response from AI")
                
        except requests.exceptions.Timeout:
            logger.error(f"Hermes API timeout for {client_id}")
            await self.send_error(client_id, "Request timed out")
        except Exception as e:
            logger.error(f"Error calling Hermes API: {e}")
            await self.send_error(client_id, "Internal server error")
    
    async def handle_audio_message(self, client_id: str, data: Dict[str, Any]):
        """Handle audio message (placeholder for future ASR integration)"""
        logger.info(f"Received audio from {client_id} (length: {len(data.get('audio_data', ''))} chars)")
        
        # For now, send a placeholder response
        websocket = self.active_connections.get(client_id)
        if websocket:
            response_data = {
                "type": "text",
                "content": "I received your audio message. Text-to-speech integration is coming soon!",
                "timestamp": datetime.now().isoformat(),
                "emotion": "neutral"
            }
            await websocket.send(json.dumps(response_data))
    
    async def handle_control_message(self, client_id: str, data: Dict[str, Any]):
        """Handle control messages"""
        action = data.get("action")
        logger.info(f"Control action from {client_id}: {action}")
        
        if action == "clear_history":
            if client_id in self.conversation_histories:
                self.conversation_histories[client_id] = []
                logger.info(f"Cleared history for {client_id}")
        
        # Forward to VTuber backend if connected
        # This is a placeholder for more advanced control features
    
    async def send_error(self, client_id: str, error_message: str):
        """Send error message to client"""
        websocket = self.active_connections.get(client_id)
        if websocket:
            error_data = {
                "type": "error",
                "content": error_message,
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(error_data))
    
    def detect_emotion(self, text: str) -> str:
        """Simple emotion detection based on keywords"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["great", "awesome", "excellent", "good", "happy", "love"]):
            return "happy"
        elif any(word in text_lower for word in ["sorry", "unfortunately", "bad", "wrong", "sad", "disappoint"]):
            return "sad"
        elif any(word in text_lower for word in ["wow", "oh", "really", "amazing", "surprising"]):
            return "surprised"
        elif any(word in text_lower for word in ["hmm", "let me think", "interesting", "consider"]):
            return "thinking"
        else:
            return "neutral"
    
    async def start_server(self):
        """Start the WebSocket proxy server"""
        logger.info(f"Starting Hermes Proxy on ws://{self.config.proxy_host}:{self.config.proxy_port}")
        logger.info(f"Hermes Agent URL: {self.config.hermes_url}")
        
        server = await websockets.serve(
            self.handle_client,
            self.config.proxy_host,
            self.config.proxy_port
        )
        
        logger.info("Proxy server is running. Press Ctrl+C to stop.")
        
        try:
            await server.wait_closed()
        except asyncio.CancelledError:
            logger.info("Shutting down proxy server...")
            server.close()
            await server.wait_closed()

def load_config(config_file: str = "proxy_config.json") -> ProxyConfig:
    """Load configuration from file or use defaults"""
    import os
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            return ProxyConfig(**config_data)
        except Exception as e:
            logger.warning(f"Could not load config from {config_file}: {e}")
    
    # Return default config
    return ProxyConfig()

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Open-LLM-VTuber + Hermes Agent Proxy")
    parser.add_argument("--hermes-url", default="http://localhost:8000", help="Hermes Agent URL")
    parser.add_argument("--host", default="localhost", help="Proxy host")
    parser.add_argument("--port", type=int, default=8765, help="Proxy port")
    parser.add_argument("--config", default="proxy_config.json", help="Configuration file")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override with command line arguments
    if args.hermes_url != "http://localhost:8000":
        config.hermes_url = args.hermes_url
    if args.host != "localhost":
        config.proxy_host = args.host
    if args.port != 8765:
        config.proxy_port = args.port
    
    # Create and start proxy
    proxy = HermesProxy(config)
    
    try:
        await proxy.start_server()
    except KeyboardInterrupt:
        logger.info("Proxy server stopped by user")
    except Exception as e:
        logger.error(f"Proxy server error: {e}")
        raise

if __name__ == "__main__":
    print("=" * 60)
    print("Open-LLM-VTuber + Hermes Agent WebSocket Proxy")
    print("=" * 60)
    print()
    print("This proxy bridges Open-LLM-VTuber with Hermes Agent.")
    print()
    print("Usage:")
    print("  1. Start Hermes Agent: hermes --api-port 8000 --api-mode openai")
    print("  2. Start Open-LLM-VTuber: python run_server.py")
    print("  3. Start this proxy: python hermes_proxy.py")
    print("  4. Configure Open-LLM-VTuber to connect to ws://localhost:8765")
    print()
    print("=" * 60)
    print()
    
    asyncio.run(main())
