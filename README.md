# Open-LLM-VTuber Integration for Hermes Agent

A comprehensive skill for integrating [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) with [Hermes Agent](https://github.com/NousResearch/hermes-agent) to create AI YouTuber companions with voice interaction and Live2D avatars.

## 🚀 Features

- **Voice Interaction**: Real-time voice conversations with speech-to-text and text-to-speech
- **Live2D Avatar**: Animated virtual character that responds to conversation
- **Hermes Agent Backend**: Use Hermes as the AI brain for your VTuber
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Offline Capable**: Run completely locally with no cloud dependencies
- **Customizable Personas**: Create unique AI personalities for your VTuber
- **Streaming Ready**: Perfect for YouTube, Twitch, or Discord streaming

## 📁 Repository Structure

```
hermes-open-llm-vtuber-skill/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── references/
│   └── api-endpoints.md       # API reference documentation
└── scripts/
    ├── setup.sh               # Automated setup script
    ├── test_integration.py    # Integration testing tool
    └── hermes_proxy.py        # WebSocket proxy for bridging
```

## 🛠️ Quick Start

### Prerequisites

1. **Python 3.10+**
2. **Hermes Agent** installed ([Installation Guide](https://github.com/NousResearch/hermes-agent))
3. **Git** for cloning repositories

### Installation

```bash
# Clone this skill repository
git clone https://github.com/123mikeyd/hermes-open-llm-vtuber-skill.git
cd hermes-open-llm-vtuber-skill

# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

1. **Clone Open-LLM-VTuber**:
   ```bash
   git clone https://github.com/Open-LLM-VTuber/Open-LLM-VTuber.git
   cd Open-LLM-VTuber
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure for Hermes Agent**:
   ```bash
   cp config/hermes_integration.yaml conf.yaml
   # Edit conf.yaml as needed
   ```

4. **Start the integration**:
   ```bash
   # Terminal 1: Start Hermes Agent API
   hermes --api-port 8000 --api-mode openai
   
   # Terminal 2: Start Open-LLM-VTuber
   python run_server.py
   ```

5. **Access the web interface**:
   Open http://localhost:3000 in your browser

## 🔧 Configuration

### Basic Configuration (conf.yaml)

```yaml
system_config:
  # Use Hermes Agent as LLM backend
  llm_backend: "openai"
  openai:
    api_key: "hermes-agent"
    base_url: "http://localhost:8000/v1"
    model: "hermes-agent"
  
  # Speech-to-Text (local)
  asr_backend: "faster-whisper"
  
  # Text-to-Speech (free)
  tts_backend: "edge-tts"

character_config:
  # Your AI persona
  persona_prompt: |
    You are an AI YouTuber companion...
  
  # Live2D model
  live2d_model: "default"
```

### Advanced Options

- **Multiple Characters**: Create different conf.yaml files for different personas
- **Voice Customization**: Choose from 300+ Edge TTS voices
- **Avatar Models**: Use custom Live2D models
- **Streaming Integration**: Connect to Twitch/YouTube chat

## 🧪 Testing

Run the integration test to verify everything works:

```bash
python scripts/test_integration.py
```

This will test:
- ✅ Hermes Agent connection
- ✅ WebSocket communication
- ✅ Configuration validity
- ✅ Chat completion

## 🎭 Use Cases

### 1. AI YouTuber Companion
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

## 🔌 Integration Methods

### Method 1: OpenAI-Compatible API (Recommended)
Hermes Agent exposes an OpenAI-compatible API that Open-LLM-VTuber can use directly.

### Method 2: WebSocket Proxy
Use the included `hermes_proxy.py` for more control over the communication.

### Method 3: Direct Integration
Modify Open-LLM-VTuber's agent module for deep integration.

## 📚 Documentation

- **[SKILL.md](SKILL.md)**: Complete skill documentation
- **[API Reference](references/api-endpoints.md)**: Open-LLM-VTuber API endpoints
- **[Setup Guide](scripts/setup.sh)**: Automated setup script
- **[Test Tool](scripts/test_integration.py)**: Integration testing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) for the amazing VTuber framework
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) for the powerful AI agent
- [Live2D](https://www.live2d.com/) for the avatar technology
- [Edge TTS](https://github.com/rany2/edge-tts) for free text-to-speech

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/123mikeyd/hermes-open-llm-vtuber-skill/issues)
- **Discussions**: [GitHub Discussions](https://github.com/123mikeyd/hermes-open-llm-vtuber-skill/discussions)
- **Open-LLM-VTuber Discord**: [Join Discord](https://discord.gg/3UDA8YFDXx)
- **Hermes Agent Discord**: [Join Discord](https://discord.gg/hermes-agent)

## 🌟 Star History

If you find this project useful, please give it a star! ⭐

---

**Happy Streaming!** 🎥🎮🤖
