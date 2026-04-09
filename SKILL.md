---
name: open-llm-vtuber
description: Create an AI YouTuber companion using Open-LLM-VTuber with Hermes Agent as the backend. Features voice interaction, Live2D avatar animation, and real-time conversation capabilities.
version: 1.2.0
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

**Important Note**: Hermes Agent does not have a built-in OpenAI-compatible API server. You have several options:

**Option A: Use MCP Server (Recommended)**
```bash
# Start Hermes as an MCP server
hermes mcp serve

# This exposes Hermes conversations via Model Context Protocol
```

**Option B: Use a WebSocket Proxy**
Use the included `scripts/hermes_proxy.py` to create a bridge:
```bash
# Terminal 1: Start the proxy
python scripts/hermes_proxy.py

# Terminal 2: Configure Open-LLM-VTuber to use ws://localhost:8765
```

**Option C: Direct Integration (Advanced)**
Modify Open-LLM-VTuber to call Hermes directly via its CLI or library.

### Step 4: Launch Open-LLM-VTuber

```bash
# Start the backend server
python run_server.py

# Access the web interface
# Open http://localhost:3000 in your browser
# Or use the desktop client
```

## Testing the Integration

### Simple Test Environment (For Quick Testing)

If you want to test the concept quickly without setting up the full Open-LLM-VTuber, use the included simple test environment:

```bash
# Navigate to test directory
mkdir test-vtuber && cd test-vtuber

# Install Flask for simple web server
pip install flask

# Copy the test files from the skill
cp /path/to/skill/scripts/simple_test.html .
cp /path/to/skill/scripts/simple_backend.py .

# Run the test server
python simple_backend.py

# Open http://localhost:5000 in your browser
```

### Testing with Your Assets

To test with your own anime girl picture and song:

1. **Update the test configuration**:
   ```python
   # Edit simple_backend.py
   CONFIG = {
       'demo_mode': True,  # Start with demo mode
       'picture_path': '/path/to/your/anime-girl.png',
       'song_path': '/path/to/your/song.mp3'
   }
   ```

2. **Run the test server**:
   ```bash
   python simple_backend.py
   ```

3. **Access the interface**:
   - Open http://localhost:5000
   - Your picture will appear as the avatar
   - Your song will play as background music
   - Chat with the AI companion

### Test Files Included

The skill includes these test files:
- `scripts/simple_test.html` - Web interface with avatar and chat
- `scripts/simple_backend.py` - Flask backend for testing
- `scripts/test_integration.py` - Integration testing tool

### What You Can Test

1. **Basic Chat**: Text conversation with AI
2. **Avatar Display**: Show your anime girl picture
3. **Background Music**: Play your song
4. **API Connection**: Test connection to Hermes (if configured)

### Limitations of Test Environment

- No Live2D animation (requires specific model files)
- No real-time voice interaction (requires ASR/TTS setup)
- No lip-sync (requires TTS integration)
- Basic sentiment analysis only

For full VTuber functionality, use the complete Open-LLM-VTuber setup.

## Integration Methods

### Method 1: MCP Server Integration (Recommended)

Hermes Agent can run as an MCP (Model Context Protocol) server:

1. Start Hermes as MCP server:
   ```bash
   hermes mcp serve
   ```

2. Configure Open-LLM-VTuber to connect via MCP protocol
3. This provides the most direct integration with Hermes capabilities

### Method 2: WebSocket Proxy (Practical Alternative)

Use the included WebSocket proxy to bridge the systems:

1. Start the proxy:
   ```bash
   python scripts/hermes_proxy.py
   ```

2. Configure Open-LLM-VTuber to connect to `ws://localhost:8765`
3. The proxy handles message routing and conversation history

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

## Security & Safety Considerations

### Security Analysis
All scripts in this skill have been analyzed for security. The code:
- ✅ Only makes local network connections (localhost)
- ✅ Doesn't download external code or execute arbitrary commands
- ✅ Only communicates between your local Hermes Agent and Open-LLM-VTuber
- ✅ Doesn't access sensitive system files
- ✅ Uses well-known Python libraries (websockets, requests, asyncio)

### How to Verify Code Safety
1. **Review the code yourself**:
   ```bash
   # Check all Python files
   cat scripts/*.py
   # Check shell script
   cat scripts/setup.sh
   ```

2. **Run security scan**:
   ```bash
   # Look for suspicious patterns
   grep -r "os\.system\|subprocess\.call\|exec\|eval\|__import__" scripts/
   ```

3. **Monitor network activity**:
   ```bash
   # While running, check connections
   netstat -tulpn | grep python
   # or
   sudo lsof -i :8000  # Hermes Agent
   sudo lsof -i :3000  # Open-LLM-VTuber
   sudo lsof -i :8765  # Proxy (if used)
   ```

### Safe Usage Practices
1. **Run as non-root user** - Never run as administrator/root
2. **Use firewall rules** - Block external access to ports 8000, 3000, 8765
3. **Monitor resource usage** - Watch CPU/memory consumption
4. **Start with test conversations** - Don't send sensitive data initially
5. **Run in isolated environment** (optional) - Use VM or container for extra safety

### If You're Still Unsure
- **Run in a VM** - Isolate completely from main system
- **Use a test machine** - Don't use on production systems
- **Ask for community review** - Post on forums for others to check
- **Start small** - Test with simple conversations first

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

**GitHub Token Authentication Failed**
- Verify your GitHub personal access token has `repo` scope
- Check token expiration date (tokens can expire)
- Test token validity: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user`
- If token is invalid, generate a new one at GitHub Settings > Developer settings > Personal access tokens
- Alternative: Use SSH keys instead of HTTPS tokens for authentication
- Fallback: Create a local archive (`tar -czvf skill.tar.gz skill-directory/`) for manual upload

**Hermes API Server Not Available**
- Hermes Agent doesn't have a built-in OpenAI-compatible API server
- Use `hermes mcp serve` for MCP protocol instead
- Use the WebSocket proxy: `python scripts/hermes_proxy.py`
- For testing, use the simple Flask backend: `python scripts/simple_backend.py`

**GitHub Token Authentication Failed**
- Verify your GitHub personal access token has `repo` scope
- Check token expiration date (tokens can expire)
- Test token validity: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user`
- If token is invalid, generate a new one at GitHub Settings > Developer settings > Personal access tokens
- Alternative: Use SSH keys instead of HTTPS tokens for authentication
- Fallback: Create a local archive (`tar -czvf skill.tar.gz skill-directory/`) for manual upload

**GitHub Token Authentication Failed**
- Verify your GitHub personal access token has `repo` scope
- Check token expiration date (tokens can expire)
- Test token validity: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user`
- If token is invalid, generate a new one at GitHub Settings > Developer settings > Personal access tokens
- Alternative: Use SSH keys instead of HTTPS tokens for authentication
- Fallback: Create a local archive (`tar -czvf skill.tar.gz skill-directory/`) for manual upload

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

- **This Skill**: [GitHub Repository](https://github.com/123mikeyd/hermes-open-llm-vtuber-skill)
- [Open-LLM-VTuber Documentation](https://open-llm-vtuber.github.io/)
- [Open-LLM-VTuber GitHub](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)
- [Live2D Models](https://www.live2d.com/en/)
- [Hermes Agent Documentation](https://github.com/NousResearch/hermes-agent)

## Creating and Publishing Skills to GitHub

### Creating a Skill Repository
1. **Initialize git repository**:
   ```bash
   cd your-skill-directory
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub repository**:
   ```bash
   # Using GitHub CLI (recommended)
   gh repo create your-skill-name --public --description "Description"
   
   # Or using GitHub API
   curl -H "Authorization: token YOUR_TOKEN" \
        -d '{"name":"your-skill-name","description":"Description","private":false}' \
        https://api.github.com/user/repos
   ```

3. **Push to GitHub**:
   ```bash
   git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/your-skill-name.git
   git push -u origin main
   ```

### Handling GitHub Token Issues
If you encounter "Bad credentials" errors:
1. **Verify token validity**:
   ```bash
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
   ```

2. **Check token permissions**:
   - Token needs `repo` scope for private repositories
   - Token needs `public_repo` scope for public repositories
   - Check token expiration (tokens can expire)

3. **Alternative authentication methods**:
   - Use SSH keys: `git remote set-url origin git@github.com:USER/REPO.git`
   - Use GitHub CLI: `gh auth login`
   - Use credential helpers: `git config --global credential.helper store`

4. **Fallback option**:
   ```bash
   # Create local archive for manual upload
   tar -czvf skill-name.tar.gz skill-directory/
   # Then upload via GitHub web interface
   ```

### Skill Structure Best Practices
```
your-skill/
├── SKILL.md              # Main documentation
├── README.md             # GitHub repository readme
├── LICENSE               # License file (MIT recommended)
├── scripts/              # Executable scripts
│   ├── setup.sh          # Installation script
│   └── helper.py         # Utility scripts
├── references/           # Documentation
│   └── api-docs.md       # API documentation
└── examples/             # Usage examples
    └── config.yaml       # Example configuration
```

## Lessons Learned from Testing

### What We Discovered

1. **Hermes API Limitations**: Hermes Agent doesn't have a built-in OpenAI-compatible API server. We need to use MCP server or WebSocket proxy instead.

2. **Testing Strategy**: Start with a simple Flask backend to test concepts before setting up the full Open-LLM-VTuber system.

3. **GitHub Token Issues**: GitHub personal access tokens can expire or have insufficient permissions. Always verify token validity before pushing.

4. **Security Considerations**: Users are rightfully concerned about security. Always provide clear security analysis and verification methods.

5. **Asset Integration**: Users want to test with their own assets (pictures, songs) quickly. Provide simple test environments for this.

### Best Practices

1. **Start Simple**: Begin with the test environment before full setup
2. **Verify Connections**: Test each component separately
3. **Monitor Resources**: Watch CPU/memory usage during testing
4. **Document Issues**: Keep track of what works and what doesn't
5. **Share Learnings**: Update documentation with new insights

### Common Pitfalls to Avoid

1. **Assuming API Availability**: Don't assume Hermes has an API server
2. **Ignoring Token Expiration**: GitHub tokens expire - check them regularly
3. **Overcomplicating Setup**: Start with demo mode, then add complexity
4. **Skipping Security Review**: Always review code before running
5. **Not Testing Locally**: Test on local machine before deployment

## Next Steps

1. **Install and test** the basic integration
2. **Customize your persona** and avatar
3. **Connect to streaming platforms** if desired
4. **Share your creation** with the community!

For help and discussions:
- Open-LLM-VTuber: [Discord](https://discord.gg/3UDA8YFDXx) | [Zulip](https://olv.zulipchat.com)
- Hermes Agent: [Discord](https://discord.gg/hermes-agent)
- This Skill: [GitHub Issues](https://github.com/123mikeyd/hermes-open-llm-vtuber-skill/issues)
