# Ollama-Powered Autonomous Bot Setup

## 🚀 Quick Start with Ollama

### Prerequisites
- Node.js 18+
- Telegram account
- GitHub account
- **Ollama installed and running locally**
- **Ollama API access**

### Step 1: Fork and Clone
```bash
# Fork this repository to your account (bklyny2021)
# Clone your fork
git clone https://github.com/bklyny2021/autonomous_bot.git
cd autonomous_bot
```

### Step 2: Ollama Setup
```bash
# Ensure Ollama is installed and running
ollama list  # Verify it's working
ollama pull sara-boo1-fixed  # Download Sara model
```

### Step 3: Configure GitHub Secrets
Go to your repository > Settings > Secrets and variables > Actions:

**Required Secrets:**
- `OLLAMA_API_KEY`: Your Ollama API key (you have this)
- `OLLAMA_URL`: `http://localhost:11434` (or your Ollama instance)
- `OLLAMA_MODEL`: `sara-boo1-fixed` (or your preferred model)
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (get from @BotFather)
- `GITHUB_TOKEN`: GitHub Personal Access Token
- `ALLOWED_USERS`: Comma-separated list of Telegram user IDs

**Optional:**
- `OLLAMA_USERNAME`: If your Ollama requires auth
- `OLLAMA_PASSWORD`: If your Ollama requires auth

### Step 4: Set up Telegram Bot
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose name (e.g., "My Autonomous Bot")
4. Choose username
5. Save the bot token as a GitHub secret

### Step 5: Enable GitHub Actions
Go to Actions tab > enable workflows

### Step 6: Start Event Handler
```bash
cd event_handler
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
```

## 🌐 Ollama Configuration

### Local Ollama Setup
```bash
# Install Ollama if not already
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Verify it's running
curl http://localhost:11434/api/tags

# Pull Sara model
ollama pull sara-boo1-fixed
```

### Remote Ollama Setup
If your Ollama instance is remote:
```bash
# In GitHub secrets:
OLLAMA_URL="http://your-server:11434"
OLLAMA_MODEL="sara-boo1-fixed"
OLLAMA_API_KEY="your-api-key"
```

## 🤖 How It Works with Ollama

### Architecture
1. **Event Handler** (Node.js) -receives Telegram messages
2. **GitHub Actions** -spins up container with Ollama access
3. **Ollama Agent** -executes tasks using Sara model
4. **Pull Requests** -track all changes for review

### Ollama Integration Benefits
- **Privacy**: All AI processing stays local
- **Cost**: No per-request API costs
- **Speed**: Local inference, no network latency
- **Control**: Use any model you want
- **Offline**: Works without internet connection

### Task Flow with Ollama
1. User sends task to Telegram bot
2. Event handler creates job branch
3. GitHub Actions runs agent container
4. Agent calls local Ollama API for AI responses
5. Changes committed and PR created
6. User gets completion notification

## 🔒 Ollama Security

### What's Protected
- **API Keys** - Only process-level access
- **Model Files** - Secure container isolation
- **Network Access** - Limited to allowed destinations
- **File System** - Path restrictions enforced

### Ollama Configuration Security
```yaml
# Environment variables in workflow
env:
  OLLAMA_API_KEY: ${{ secrets.OLLAMA_API_KEY }}
  OLLAMA_URL: ${{ secrets.OLLAMA_URL }}
  OLLAMA_MODEL: ${{ secrets.OLLAMA_MODEL }}
```

### Agent Protection
- No direct Ollama system file access
- Model responses filtered for safety
- Path restrictions still apply
- Git auditing for all changes

## 🎨 Example Tasks with Ollama

### 📝 AI-Powered Content Creation
```
Write a Python script that monitors cryptocurrency prices and sends alerts
```

### 🔧 Smart Code Generation
```
Create a Discord bot that automatically manages voice channel permissions
```

### 📊 Analysis and Research
```
Research latest developments in quantum computing and create a technical report
```

### 🤖 System Automation
```
Build an automated script that backs up important files to cloud storage
```

## 🧪 Test with Ollama

### Local Testing
```bash
# Test Ollama connectivity
curl http://localhost:11434/api/generate \
  -d '{"model":"sara-boo1-fixed","prompt":"Hello Sara!"}'

# Test the agent locally
python agent/ollama_agent.py
```

### Full Integration Test
```bash
# Start event handler
cd event_handler && npm start

# Send test message to Telegram bot
echo "Create a simple hello world Python script" | telegram-cli
```

## 🔄 Migration from Cloud APIs

### Advantages of Ollama
- **No per-request costs**
- **Complete privacy**
- **Local model control**
- **Offline capability**
- **Custom fine-tuning**

### Model Management
```bash
# List available models
ollama list

# Download new models
ollama pull llama3
ollama pull codellama

# Use different models in config
# Set OLLAMA_MODEL secret in GitHub
```

### Performance Tuning
```bash
# Monitor Ollama performance
top -p $(pgrep ollama)

# Check model usage
ollama ps

# Clear GPU cache if needed
nvidia-smi --gpu-reset
```

## 🐛 Troubleshooting

### Common Ollama Issues

**Problem**: Ollama not running
```bash
# Check service status
sudo systemctl status ollama

# Start Ollama
sudo systemctl start ollama
```

**Problem**: GitHub Actions can't reach Ollama
```bash
# Need tunneling solution - see TUNNELING.md
# Or use self-hosted runner with local access
```

**Problem**: Model download slow
```bash
# Use alternative mirror or local model file
ollama import sara-boo1-fixed.model
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
python agent/ollama_agent.py
```

## 🚀 Production Deployment

### Self-Hosted Runner Setup
For best performance, use self-hosted runner:
```bash
# Install GitHub Actions runner locally
# It can access your local Ollama directly
# No networking issues
# Full performance
```

### Cloud Alternative
If using cloud runner:
- Set up Ollama on cloud server
- Configure firewall for GitHub runner access
- Use secure tunnel or VPN

## 📚 Advanced Features

### Custom Models
```bash
# Use fine-tuned models
OLLAMA_MODEL="my-custom-sara"

# Model switching based on task type
# Configure in agent logic
```

### Multi-Model Support
```python
# In ollama_agent.py - model selection
if task_type == "coding":
    model = "codellama"
elif task_type == "analysis":
    model = "llama3"
else:
    model = "sara-boo1-fixed"
```

### Performance Monitoring
```bash
# Monitor Ollama requests
tail -f ~/.ollama/logs/server.log

# Check model performance
time ollama run sara-boo1-fixed "test prompt"
```

## 🛠️ Integration Examples

### Discord Integration
```python
# Use Ollama agent for Discord bot responses
response = ollama_agent.process_message(
    user_message,
    context="discord_chat"
)
```

### Web Interface Integration
```python
# Flask endpoint with Ollama
@app.route('/chat', methods=['POST'])
def chat():
    response = ollama_agent.execute_task(request.json['message'])
    return jsonify({"response": response})
```

### CLI Tool Integration
```python
# Command line interface
parser = argparse.ArgumentParser()
parser.add_argument('task')
args = parser.parse_args()

agent = OllamaAgent()
result = agent.execute_task(args.task)
print(result['summary'])
```

---

**Next Steps**: After setup, send your first task to the Telegram bot and watch your locally-powered autonomous AI assistant at work! 🚀

**Key Advantage**: All AI processing happens on YOUR infrastructure with Ollama! ✨