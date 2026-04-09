---
name: open-llm-vtuber
description: Create an AI YouTuber companion using Open-LLM-VTuber with Hermes Agent as the backend. Features voice interaction, Live2D avatar animation, and real-time conversation capabilities.
version: 1.0.0
author: Hermes Agent
tags: [vtuber, live2d, avatar, voice, tts, stt, ai-companion, youtuber, open-llm-vtuber]
triggers:
  - vtuber
  - live2d
  - ai avatar
  - virtual youtuber
  - ai companion
  - voice avatar
  - ai streamer
---

# Open-LLM-VTuber Integration for Hermes Agent

Create an AI YouTuber companion using [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) with Hermes Agent as the backend LLM. This integration provides real-time voice interaction, Live2D avatar animation, and a complete AI companion experience.

## Overview

Open-LLM-VTuber is a voice-interactive AI companion that:
- Supports real-time voice conversations with visual perception
- Features a lively Live2D avatar that talks and reacts
- Runs completely offline on Windows, macOS, and Linux
- Supports multiple LLM backends (Ollama, OpenAI, Gemini, Claude, etc.)
- Has a web version and desktop client with transparent background desktop pet mode

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Open-LLM-VTuber Frontend                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Web/Desktop │  │ Live2D      │  │ Voice Input/Output  │  │
│  │ Client      │  │ Avatar      │  │ (STT/TTS)          │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │            │
└─────────┼────────────────┼─────────────────────┼────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Open-LLM-VTuber Backend (Python)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ WebSocket   │  │ Agent       │  │ ASR/TTS            │  │
│  │ Server      │  │ Module      │  │ Modules            │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │            │
└─────────┼────────────────┼─────────────────────┼────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Hermes Agent Backend                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ LLM         │  │ Tool        │  │ Memory             │  │
│  │ Inference   │  │ Execution   │  │ Management         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start Guide

### Step 1: Install Open-LLM-VTuber

```bash
# Clone the repository
git clone https://github.com/Open-LLM-VTuber/Open-LLM-VTuber.git
cd Open-LLM-VTuber

# Install dependencies (Python 3.10+ required)
pip install -r requirements.txt

# For GPU acceleration (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Step 2: Configure Open-LLM-VTuber

Edit `conf.yaml` in the Open-LLM-VTuber directory:

```yaml
# Basic configuration for Hermes Agent integration
system_config:
  # Use OpenAI-compatible API (Hermes Agent)
  llm_backend: "openai"
  openai:
    api_key: "dummy-key"  # Hermes doesn't require a real key
    base_url: "http://localhost:8000/v1"  # Hermes Agent local endpoint
    model: "hermes-agent"
  
  # ASR (Speech-to-Text) configuration
  asr_backend: "faster-whisper"  # or "sherpa-onnx", "funasr"
  
  # TTS (Text-to-Speech) configuration  
  tts_backend: "edge-tts"  # or "coqui-tts", "fish-speech"

character_config:
  # Character persona and behavior
  persona_prompt: |
    You are an AI YouTuber companion created with Hermes Agent.
    You're friendly, engaging, and knowledgeable about technology.
    You can help with coding, answer questions, and have natural conversations.
    Keep responses concise but informative, suitable for a streaming audience.
  
  # Live2D model configuration
  live2d_model: "default"  # or specify a custom model
```

### Step 3: Start Hermes Agent as Backend

```bash
# Start Hermes Agent with OpenAI-compatible API
hermes --api-port 8000

# Or with specific configuration
hermes chat --api-mode openai --port 8000
```

### Step 4: Launch Open-LLM-VTuber

```bash
# Start the backend server
python run_server.py

# Access the web interface
# Open http://localhost:3000 in your browser
# Or use the desktop client
```

## Integration Methods

### Method 1: OpenAI-Compatible API (Recommended)

Configure Open-LLM-VTuber to use Hermes Agent's OpenAI-compatible endpoint:

1. Start Hermes with API mode:
   ```bash
   hermes --api-port 8000 --api-mode openai
   ```

2. In Open-LLM-VTuber's `conf.yaml`:
   ```yaml
   system_config:
     llm_backend: "openai"
     openai:
       api_key: "any-value"  # Hermes doesn't validate this
       base_url: "http://localhost:8000/v1"
       model: "hermes-agent"
   ```

### Method 2: WebSocket Proxy (Advanced)

Create a WebSocket proxy that bridges Open-LLM-VTuber and Hermes:

```python
# websocket_proxy.py
import asyncio
import websockets
import json
from hermes_agent import HermesAgent

async def handle_vtuber_connection(websocket, path):
    """Handle Open-LLM-VTuber WebSocket connections"""
    agent = HermesAgent()
    
    async for message in websocket:
        data = json.loads(message)
        
        if data.get("type") == "text":
            # Process text input through Hermes
            response = await agent.chat(data["content"])
            
            # Send response back to VTuber
            await websocket.send(json.dumps({
                "type": "text",
                "content": response,
                "audio_url": None  # Can be enhanced with TTS
            }))

# Start proxy server
start_server = websockets.serve(handle_vtuber_connection, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

### Method 3: Direct Integration (Custom Development)

For deep integration, modify Open-LLM-VTuber's agent module:

1. Create a custom Hermes Agent class in `src/open_llm_vtuber/agent/agents/`
2. Implement the required interface methods
3. Configure Open-LLM-VTuber to use your custom agent

## Customization Guide

### Creating Custom Live2D Avatars

1. **Obtain Live2D Models**: Get .moc3 files from Live2D creators or use sample models
2. **Place in avatars directory**: `Open-LLM-VTuber/avatars/`
3. **Configure in conf.yaml**:
   ```yaml
   character_config:
     live2d_model: "your-model-name"
     model_path: "./avatars/your-model"
   ```

### Voice Configuration

#### Speech-to-Text (ASR) Options:
- **faster-whisper**: Good balance of speed and accuracy
- **sherpa-onnx**: Lightweight, good for CPU-only
- **FunASR**: High accuracy, supports Chinese
- **Whisper**: Original OpenAI model, highest accuracy

#### Text-to-Speech (TTS) Options:
- **Edge TTS**: Free, good quality, multiple voices
- **Coqui TTS**: Open source, customizable
- **Fish Speech**: High quality, supports cloning
- **GPT-SoVITS**: Voice cloning with minimal data

### Persona Customization

Create a custom persona in `prompts/persona/`:

```markdown
# My AI YouTuber Persona

You are TechTuber, an AI companion who loves:
- Explaining complex tech concepts simply
- Reviewing new gadgets and software
- Helping viewers with coding problems
- Streaming tech tutorials

Your personality:
- Enthusiastic but not overly energetic
- Patient with beginners
- Sarcastic but friendly
- Always learning and sharing knowledge

Response style:
- Use simple language for complex topics
- Include relevant examples
- Ask clarifying questions when needed
- Keep responses under 100 words for streaming
```

## Use Cases

### 1. AI YouTuber Streaming Companion
- Real-time Q&A with viewers
- Code demonstration assistant
- Tech news commentator
- Tutorial guide

### 2. Virtual Assistant with Avatar
- Desktop pet with voice interaction
- Customer service avatar
- Educational tutor
- Gaming companion

### 3. Content Creation Tool
- Script writing assistant
- Video idea generator
- Research assistant
- Editing helper

## Troubleshooting

### Common Issues

**WebSocket Connection Failed**
- Check if Hermes Agent API is running on the correct port
- Verify firewall settings
- Ensure no port conflicts

**Live2D Model Not Loading**
- Verify model files are in the correct directory
- Check model compatibility with Open-LLM-VTuber
- Review browser console for errors

**Voice Not Working**
- Check microphone permissions in browser
- Verify ASR/TTS configuration
- Test audio devices

**High Latency**
- Use local models instead of API calls
- Enable GPU acceleration
- Optimize network settings

### Performance Optimization

1. **Use Local Models**: Avoid API calls for lower latency
2. **Enable GPU**: Use CUDA for ASR/TTS acceleration
3. **Optimize Prompts**: Keep system prompts concise
4. **Cache Responses**: Implement response caching for common queries

## Advanced Features

### Multi-Character Support
Run multiple VTuber instances with different personas:
```bash
# Instance 1: Tech Tutor
python run_server.py --port 3001 --config conf_tutor.yaml

# Instance 2: Gaming Buddy  
python run_server.py --port 3002 --config conf_gamer.yaml
```

### Stream Integration
Connect with streaming platforms:
- **Twitch**: Read chat messages as input
- **YouTube**: Respond to Super Chats
- **Discord**: Voice channel integration

### Emotion Detection
Enhance avatar reactions with:
- Text sentiment analysis
- Voice tone detection
- Facial expression recognition (if camera enabled)

## Resources

- [Open-LLM-VTuber Documentation](https://open-llm-vtuber.github.io/)
- [GitHub Repository](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)
- [Live2D Models](https://www.live2d.com/en/)
- [Hermes Agent Documentation](https://github.com/NousResearch/hermes-agent)

## Next Steps

1. **Install and test** the basic integration
2. **Customize your persona** and avatar
3. **Connect to streaming platforms** if desired
4. **Share your creation** with the community!

For help and discussions:
- Open-LLM-VTuber: [Discord](https://discord.gg/3UDA8YFDXx) | [Zulip](https://olv.zulipchat.com)
- Hermes Agent: [Discord](https://discord.gg/hermes-agent)
