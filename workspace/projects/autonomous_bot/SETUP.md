# Autonomous Bot Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Telegram account
- GitHub account
- Anthropic API key

### Step 1: Fork and Clone
```bash
# Fork this repository to your account
# Clone your fork
git clone https://github.com/YOUR_USERNAME/autonomous_bot.git
cd autonomous_bot
```

### Step 2: Configure GitHub Secrets
Go to your repository > Settings > Secrets and variables > Actions

Add these secrets:
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (get from @BotFather)
- `GITHUB_TOKEN`: GitHub Personal Access Token
- `ALLOWED_USERS`: Comma-separated list of Telegram user IDs

### Step 3: Set up Telegram Bot
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose a name (e.g., "My Autonomous Bot")
4. Save the bot token as a GitHub secret

### Step 4: Enable GitHub Actions
Go to Actions tab > enable workflows

### Step 5: Start Event Handler
```bash
cd event_handler
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
```

## 🤖 How It Works

### Architecture
1. **Event Handler** (Node.js) - Receives Telegram messages
2. **GitHub Actions** - Runs autonomous agent securely  
3. **Docker Agent** - Executes tasks with AI integration
4. **Pull Requests** - All changes tracked and reviewable

### Security Features
- **Process-level security** - AI cannot access secrets
- **Path restrictions** - Only modify allowed directories
- **Git auditing** - Every change is committed and reviewable
- **No credential exposure** - Secrets filtered before AI execution

### Task Flow
1. User sends task to Telegram bot
2. Event handler creates job branch
3. GitHub Actions runs Docker agent
4. Agent executes task using AI
5. Changes commited and PR created
6. User gets completion notification

## Customization

### Agent Personality
Edit `agent/config/agent_config.json` to customize:
- Agent name and personality
- Available skills and capabilities
- Security restrictions
- Memory system settings

### Allowed Paths
Modify `config/ALLOWED_PATHS` to control which directories the agent can modify:
```
agent/
docs/
tools/
scripts/
```

### Skills Development
Add new skills in `agent/skills/` directory:
```python
class CustomSkill:
    def execute(self, task):
        # Your skill implementation
        return {"success": True, "result": "completed"}
```

## Advanced Features

### Self-Improvement
The agent can modify its own code through pull requests:
- Agent creates improvements via AI
- Changes are tracked in git history
- Human review prevents harmful modifications

### Memory System
Agent remembers:
- Previous task executions
- User preferences and feedback
- Learning from successful patterns
- Context for future tasks

### Parallel Processing
Multiple jobs can run simultaneously:
- Each job gets unique branch
- Isolated Docker containers
- Concurrent task execution

## Troubleshooting

### Common Issues

**Problem**: Actions not enabled in fork
**Solution**: Go to Actions tab > I understand my workflows, please enable them

**Problem**: Telegram bot not responding
**Solution**: Check bot token and ensure user ID is in `ALLOWED_USERS`

**Problem**: Agent failing to execute
**Solution**: Check GitHub Actions logs for detailed error messages

### Debug Mode
Enable debug by setting environment variable:
```bash
export DEBUG=true
npm start
```

## Security Considerations

### What's Protected
- API keys and secrets (filtered at process level)
- System files and directories
- Network configuration
- Other user accounts

### What's Allowed
- Code creation and modification
- File operations in safe directories
- Documentation generation
- Task completion and automation

### Auditing
Every agent action creates:
- Git commit with detailed message
- Pull request for human review
- Complete audit trail in repository
- Notification of job completion

## Production Deployment

### Repository Settings
- Enable branch protection on main
- Require PR reviews before merge
- Set up auto-merge for agent PRs (optional)
- Configure repository rules

### Scaling
- GitHub Actions provides free compute
- 2000 minutes/month on free plan
- More available with paid plans
- No infrastructure costs

### Monitoring
- Check Actions tab for job status
- Use `/status` command in Telegram
- Review PRs for agent changes
- Monitor repository activity

## Support

- Check GitHub Actions logs for errors
- Review created pull requests
- Validate configuration in repository secrets
- Ensure all prerequisites are installed

---

**Next Steps**: After setup, send your first task to the Telegram bot and watch your autonomous AI assistant at work! 🚀