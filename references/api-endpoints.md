# Open-LLM-VTuber API Endpoints Reference

## WebSocket API

### Connection
```
ws://localhost:3000/client-ws
```

### Message Types

#### Text Message (Client to Server)
```json
{
  "type": "text",
  "content": "Hello, how are you?",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Text Response (Server to Client)
```json
{
  "type": "text",
  "content": "I'm doing well, thank you for asking!",
  "timestamp": "2024-01-01T12:00:01Z",
  "emotion": "happy",
  "audio_url": "/audio/response_123.wav"
}
```

#### Audio Message (Client to Server)
```json
{
  "type": "audio",
  "audio_data": "base64_encoded_audio",
  "format": "wav",
  "sample_rate": 16000
}
```

#### Control Messages
```json
// Character switching
{
  "type": "control",
  "action": "switch_character",
  "character_id": "tech_tutor"
}

// Emotion override
{
  "type": "control",
  "action": "set_emotion",
  "emotion": "excited"
}

// Stop speaking
{
  "type": "control",
  "action": "stop_speaking"
}
```

## REST API Endpoints

### Health Check
```
GET /health
Response: {"status": "ok", "version": "1.0.0"}
```

### Character List
```
GET /characters
Response: {
  "characters": [
    {
      "id": "default",
      "name": "Default Character",
      "model": "default.moc3",
      "persona": "Friendly AI assistant"
    }
  ]
}
```

### Audio File Serving
```
GET /audio/{filename}
Response: WAV audio file
```

## Integration with Hermes Agent

### Using OpenAI-Compatible Endpoint

Hermes Agent can serve as the LLM backend by exposing an OpenAI-compatible API:

```bash
# Start Hermes with OpenAI-compatible API
hermes --api-port 8000 --api-mode openai
```

### Configuration Example

```yaml
# In Open-LLM-VTuber conf.yaml
system_config:
  llm_backend: "openai"
  openai:
    api_key: "dummy-key"
    base_url: "http://localhost:8000/v1"
    model: "hermes-agent"
    max_tokens: 1000
    temperature: 0.7
```

### Custom Agent Implementation

For direct integration, create a custom agent class:

```python
# src/open_llm_vtuber/agent/agents/hermes_agent.py
from .base import BaseAgent
import requests
import json

class HermesAgent(BaseAgent):
    def __init__(self, config):
        self.api_url = config.get("hermes_api_url", "http://localhost:8000")
        self.conversation_history = []
    
    async def generate_response(self, user_input):
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Call Hermes API
        response = requests.post(
            f"{self.api_url}/v1/chat/completions",
            json={
                "model": "hermes-agent",
                "messages": self.conversation_history,
                "max_tokens": 500
            }
        )
        
        data = response.json()
        assistant_message = data["choices"][0]["message"]["content"]
        
        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
```

## Error Codes

| Code | Description |
|------|-------------|
| 1000 | Normal closure |
| 1001 | Going away |
| 1002 | Protocol error |
| 1003 | Unsupported data |
| 1005 | No status received |
| 1006 | Abnormal closure |
| 1007 | Invalid frame payload data |
| 1008 | Policy violation |
| 1009 | Message too big |
| 1010 | Mandatory extension |
| 1011 | Internal server error |

## Rate Limiting

Default rate limits:
- Text messages: 10 per second
- Audio messages: 5 per second  
- API calls: 100 per minute

## Security Considerations

1. **HTTPS Required**: Microphone access requires secure context
2. **CORS Configuration**: Configure allowed origins in production
3. **Authentication**: Implement API keys for public deployments
4. **Input Validation**: Sanitize all user inputs
5. **Rate Limiting**: Prevent abuse with request limits
