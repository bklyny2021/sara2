# 🤖 Autonomous AI Bot

> Secure, autonomous AI agents that run on GitHub Actions - completely free!

## ✨ Features

### 🔐 **Security-First Design**
- **Process-level secrets filtering** - AI literally cannot access your credentials
- **Repository as agent state** - Every action is a git commit and audit trailer
- **Path restrictions** - Agent only modifies safe directories
- **Pull request workflow** - All changes require human review

### 🚀 **Autonomous Operation**
- **GitHub Actions integration** - Free compute 2000+ minutes/month
- **Self-evolving** - Agent improves its own code via pull requests
- **Parallel processing** - Multiple jobs run simultaneously
- **Telegram interface** - Simple command-based interaction

### 🧠 **AI-Powered**
- **Sara personality** - Enthusiastic AI assistant with creative problem-solving
- **Memory system** - Learns from all interactions and tasks
- **Task analysis** - Automatically determines best approach for any request
- **Skill expansion** - Agent can develop new capabilities

## 🎯 How It Works

```
┌─────────────────┐    1    ┌─────────────────┐
│   Telegram      │ ◀───── │ Agent Job      │
│   User          │         │ Completed      │
└─────────────────┘         └────────┬────────┘
         │ 5                          │
         │ (notification)             │
         ▼                             │
┌─────────────────┐    4    ┌────────▼────────┐
│   GitHub        │ ◀───── │ Pull Request   │
│   Merge           │         │ Created       │
└─────────────────┘         └─────────────────┘
         ▲ 2                           │
         │ (job created)               │
┌─────────────────┐    3    ┌───────┐          │
│   Event         │ ◀───── │ Docker │          │
│   Handler       │         │ Agent  │          │
└─────────────────┘         └───────┘          │
```

## 🛠️ Quick Start

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/autonomous_bot.git
cd autonomous_bot
```

### 2. Configure Secrets
Go to repository > Settings > Secrets and variables > Actions:

- `ANTHROPIC_API_KEY`: Required – Get from [Anthropic Console](https://console.anthropic.com/)
- `TELEGRAM_BOT_TOKEN`: Required – Create bot with @BotFather
- `GITHUB_TOKEN`: Required – Personal access token with repo scope
- `ALLOWED_USERS`: Optional – Comma-separated Telegram user IDs

### 3. Create Telegram Bot
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose name and username
4. Save bot token as GitHub secret

### 4. Enable Actions & Start
```bash
# Enable GitHub Actions (visit Actions tab in your fork)
cd event_handler
npm install
npm run setup
```

### 5. Send Your First Task!
Message your Telegram bot:
```
Create a Python script that sends daily motivational quotes
```

## 🎨 Example Tasks

### 📝 Content Creation
```
Write a blog post about the benefits of autonomous AI agents
```

### 🔧 Code Development
```
Create a web scraper that monitors prices and sends alerts
```

### 📊 Data Analysis
```
Build a dashboard to track cryptocurrency prices with charts
```

### 🤖 Automation Tools
```
Make a Discord bot that manages voice channel permissions
```

### 📚 Research & Documentation
```
Research and document the latest developments in quantum computing
```

## 🔒 Security Model

### What's Protected
- **API Keys** - Filtered at process level before AI execution
- **System Files** - Path restrictions prevent system access
- **User Data** - Only safe directories accessible
- **Network Config** - No network configuration changes
- **Credentials** - Never exposed to AI agent

### What's Allowed
- **Code Creation** - Safe file generation in allowed paths
- **Documentation** - Markdown, reports, analysis
- **Tools & Scripts** - Utility development and automation
- **Self-Improvement** - Agent can modify own code via PRs

### Auditing & Control
- **Git History** - Every action tracked and reversible
- **Pull Requests** - All changes require human review
- **Branch Isolation** - Each job runs in separate branch
- **Audit Trail** - Complete history of all agent actions

## 🏗️ Architecture

### Event Handler (Node.js)
- Receives Telegram messages
- Creates GitHub job branches
- Triggers GitHub Actions
- Sends completion notifications

### Autonomous Agent (Python)
- AI-powered task execution
- File creation and modification
- Memory system integration
- Pull request generation

### GitHub Actions
- Free compute environment
- Secure Docker container execution
- Parallel job processing
- Workflow automation

### Security Layer
- Process-level secrets filtering
- Path restrictions and validation
- Git-based auditing and review
- Branch isolation for safety

## 🧪 Local Development

```bash
# Test the agent locally
python test_agent.py

# Test event handler
cd event_handler
npm install
npm start
```

## 📚 Documentation

- [**Setup Guide**](SETUP.md) - Complete installation and configuration
- [**Architecture**](docs/ARCHITECTURE.md) - Detailed system design
- [**Security**](docs/SECURITY.md) - Security model and best practices
- [**Customization**](docs/CUSTOMIZATION.md) - Personality and skill development
- [**Auto-Merge**](docs/AUTO_MERGE.md) - Automated PR merging

## 🚀 Advanced Features

### Self-Evolving Capability
The agent can improve itself:
- Analyzes task execution patterns
- Identifies areas for improvement
- Creates pull requests with enhancements
- Learns from successful approaches

### Memory System
- Persistent memory across all interactions
- Context preservation for complex tasks
- Learning from user feedback
- Personalization and adaptation

### Parallel Processing
- Multiple tasks execute simultaneously
- Each job in isolated Docker environment
- No interference between concurrent jobs
- Scalable processing capacity

### Custom Skills Development
```python
# agent/skills/custom_skill.py
class CustomSkill:
    def execute(self, task):
        # Your custom implementation
        return {"success": True, "result": "completed"}
```

## 💰 Pricing

### Free Tier (GitHub)
- **Public Repositories**: Unlimited
- **Private Repositories**: 2000 minutes/month
- **Infrastructure**: $0 (GitHub Actions included)
- **Scaling**: More minutes available with paid plans

### Paid Alternatives
- **Other Platforms**: $20-100+/month
- **Dedicated Servers**: $50-200+/month
- **Cloud Functions**: $10-50/month

## 🛠️ Customization

### Agent Personality
Edit `agent/config/agent_config.json`:
```json
{
  "name": "Your Assistant Name",
  "personality": "Friendly and professional",
  "capabilities": ["coding", "writing", "analysis"]
}
```

### Security Boundaries
Modify `config/ALLOWED_PATHS`:
```
# Safe directories agent can modify
agent/
docs/
tools/
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement your enhancement
4. Create pull request
5. Review and merge

## 📄 License

MIT License - Feel free to use, modify, and distribute

## ⚠️ Disclaimer

This is an autonomous AI system. Always review pull requests before merging. The agent is designed to be secure but always exercise caution with automated systems.

---

## 🤔 Why This Matters

Traditional AI assistants require:
- ✅ Server costs and infrastructure
- ❌ Manual API key management
- ❌ Security risks and exposure
- ❌ Limited compute capacity

ThePopeBot provides:
- ✅ **Zero infrastructure costs**
- ✅ **Enterprise-grade security**
- ✅ **Unlimited compute capacity**
- ✅ **Complete audit trails**
- ✅ **Self-improving capability**

Join the autonomous AI revolution! 🚀