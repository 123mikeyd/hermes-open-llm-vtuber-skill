#!/bin/bash
# Open-LLM-VTuber + Hermes Agent Integration Setup Script
# This script helps set up the integration between Open-LLM-VTuber and Hermes Agent

set -e  # Exit on error

echo "=========================================="
echo "Open-LLM-VTuber + Hermes Agent Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.10 or higher."
    exit 1
}

# Check if Hermes Agent is installed
echo "Checking Hermes Agent installation..."
if command -v hermes &> /dev/null; then
    echo "✓ Hermes Agent is installed"
    hermes --version
else
    echo "⚠ Hermes Agent not found in PATH"
    echo "Please install Hermes Agent first:"
    echo "  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
    echo ""
    read -p "Continue without Hermes Agent? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create working directory
WORK_DIR="$HOME/open-llm-vtuber-hermes"
echo "Creating working directory: $WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Clone Open-LLM-VTuber if not exists
if [ ! -d "Open-LLM-VTuber" ]; then
    echo "Cloning Open-LLM-VTuber repository..."
    git clone https://github.com/Open-LLM-VTuber/Open-LLM-VTuber.git
    cd Open-LLM-VTuber
else
    echo "Open-LLM-VTuber already exists, updating..."
    cd Open-LLM-VTuber
    git pull
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found"
    echo "Installing basic dependencies..."
    pip install websockets pyyaml requests
fi

# Create configuration directory
echo "Setting up configuration..."
mkdir -p config

# Create sample configuration for Hermes integration
cat > config/hermes_integration.yaml << 'EOF'
# Open-LLM-VTuber Configuration for Hermes Agent Integration
# Copy this file to conf.yaml and modify as needed

system_config:
  # Server settings
  host: "0.0.0.0"
  port: 3000
  debug: false
  
  # LLM Backend - Use Hermes Agent via OpenAI-compatible API
  llm_backend: "openai"
  openai:
    api_key: "hermes-agent"  # Can be any value
    base_url: "http://localhost:8000/v1"
    model: "hermes-agent"
    max_tokens: 1000
    temperature: 0.7
    top_p: 0.9
  
  # ASR (Speech-to-Text) - Using local faster-whisper
  asr_backend: "faster-whisper"
  faster_whisper:
    model_size: "base"  # tiny, base, small, medium, large-v3
    device: "cpu"  # cpu or cuda
    compute_type: "int8"
  
  # TTS (Text-to-Speech) - Using Edge TTS (free)
  tts_backend: "edge-tts"
  edge_tts:
    voice: "en-US-AriaNeural"  # Many voices available
    rate: "+0%"
    volume: "+0%"
  
  # WebSocket settings
  websocket:
    ping_interval: 20
    ping_timeout: 10
    close_timeout: 5

character_config:
  # Character persona
  persona_prompt: |
    You are an AI YouTuber companion created with Hermes Agent.
    You're friendly, engaging, and knowledgeable about technology.
    You can help with coding, answer questions, and have natural conversations.
    Keep responses concise but informative, suitable for a streaming audience.
  
  # Live2D model settings
  live2d_model: "default"
  model_path: "./live2d-models/default"
  
  # Voice settings
  default_emotion: "neutral"
  emotion_mapping:
    happy: ["great", "awesome", "excellent", "good"]
    sad: ["sorry", "unfortunately", "bad", "wrong"]
    surprised: ["wow", "oh", "really", "amazing"]
    thinking: ["hmm", "let me think", "interesting"]

frontend_config:
  # Web frontend settings
  web:
    enabled: true
    port: 3000
    static_files: "./frontend"
  
  # Desktop client settings
  desktop:
    enabled: false
    transparent_background: true
    always_on_top: true

logging:
  level: "INFO"
  file: "./logs/open-llm-vtuber.log"
  max_size_mb: 10
  backup_count: 5
EOF

echo "✓ Created sample configuration: config/hermes_integration.yaml"

# Create startup script
cat > start_with_hermes.sh << 'EOF'
#!/bin/bash
# Start Open-LLM-VTuber with Hermes Agent integration

echo "Starting Open-LLM-VTuber + Hermes Agent Integration"
echo "=================================================="

# Check if Hermes Agent is running
if ! curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "Starting Hermes Agent API on port 8000..."
    hermes --api-port 8000 --api-mode openai &
    HERMES_PID=$!
    echo "Hermes Agent started with PID: $HERMES_PID"
    
    # Wait for Hermes to start
    echo "Waiting for Hermes Agent to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
            echo "✓ Hermes Agent is ready"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            echo "Error: Hermes Agent failed to start"
            exit 1
        fi
    done
else
    echo "✓ Hermes Agent is already running on port 8000"
fi

# Copy configuration if needed
if [ ! -f "conf.yaml" ]; then
    echo "Copying Hermes integration configuration..."
    cp config/hermes_integration.yaml conf.yaml
    echo "✓ Configuration copied to conf.yaml"
    echo "Please review and edit conf.yaml as needed"
fi

# Start Open-LLM-VTuber
echo "Starting Open-LLM-VTuber..."
python run_server.py

# Cleanup on exit
cleanup() {
    echo "Cleaning up..."
    if [ ! -z "$HERMES_PID" ]; then
        kill $HERMES_PID 2>/dev/null
        echo "Stopped Hermes Agent"
    fi
}

trap cleanup EXIT
EOF

chmod +x start_with_hermes.sh
echo "✓ Created startup script: start_with_hermes.sh"

# Create README for the integration
cat > INTEGRATION_README.md << 'EOF'
# Open-LLM-VTuber + Hermes Agent Integration

This directory contains everything needed to run Open-LLM-VTuber with Hermes Agent as the LLM backend.

## Quick Start

1. **Start the integration:**
   ```bash
   ./start_with_hermes.sh
   ```

2. **Access the web interface:**
   Open http://localhost:3000 in your browser

3. **Talk to your AI companion:**
   - Use the microphone to speak
   - Type messages in the chat
   - Watch the Live2D avatar respond

## Configuration

Edit `conf.yaml` to customize:

- **LLM Settings**: Adjust Hermes Agent connection
- **Voice Settings**: Change TTS voice and ASR model
- **Character**: Modify persona and avatar
- **Frontend**: Configure web/desktop client

## Useful Commands

```bash
# Start only Hermes Agent API
hermes --api-port 8000 --api-mode openai

# Start only Open-LLM-VTuber (requires Hermes running)
python run_server.py

# Test the connection
curl http://localhost:8000/v1/models

# View logs
tail -f logs/open-llm-vtuber.log
```

## Troubleshooting

### Connection Issues
- Ensure Hermes Agent is running on port 8000
- Check firewall settings
- Verify no port conflicts

### Audio Issues
- Grant microphone permissions in browser
- Check audio device settings
- Verify ASR/TTS configuration

### Performance Issues
- Use local models instead of API calls
- Enable GPU acceleration if available
- Reduce model sizes for faster response

## Resources

- [Open-LLM-VTuber Documentation](https://open-llm-vtuber.github.io/)
- [Hermes Agent Documentation](https://github.com/NousResearch/hermes-agent)
- [Live2D Models](https://www.live2d.com/en/)
EOF

echo "✓ Created integration README: INTEGRATION_README.md"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the integration:"
echo "  cd $WORK_DIR/Open-LLM-VTuber"
echo "  ./start_with_hermes.sh"
echo ""
echo "Files created:"
echo "  - config/hermes_integration.yaml  (Sample configuration)"
echo "  - start_with_hermes.sh           (Startup script)"
echo "  - INTEGRATION_README.md          (Documentation)"
echo ""
echo "Next steps:"
echo "1. Review and edit conf.yaml (created from sample)"
echo "2. Ensure Hermes Agent is installed"
echo "3. Run ./start_with_hermes.sh"
echo ""
echo "For help, see INTEGRATION_README.md"
echo "=========================================="
