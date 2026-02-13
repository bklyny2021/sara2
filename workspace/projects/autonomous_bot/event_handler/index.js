const express = require('express');
const bodyParser = require('body-parser');
const TelegramBot = require('node-telegram-bot-api');
const { Octokit } = require('@octokit/rest');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8080;

// Telegram Bot
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN);

// GitHub Client
const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
  owner: process.env.GITHUB_OWNER || 'your-username',
  repo: process.env.GITHUB_REPO || 'autonomous-bot'
});

// Allowed users for security
const ALLOWED_USERS = (process.env.ALLOWED_USERS || '').split(',').map(u => u.trim());

// Security: Verify user is allowed
function isUserAllowed(userId) {
  // If no allowed users specified, allow all (debug mode)
  if (!process.env.ALLOWED_USERS || ALLOWED_USERS.length === 0) {
    return true;
  }
  return ALLOWED_USERS.includes(userId.toString());
}

// Security: Filter sensitive information
function sanitizeTask(task) {
  // Remove potential sensitive patterns
  const cleaned = task
    .replace(/token\s*=\s*\S+/gi, 'token=REDACTED')
    .replace(/key\s*=\s*\S+/gi, 'key=REDACTED')
    .replace(/password\s*=\s*\S+/gi, 'password=REDACTED');
  
  return cleaned;
}

// Create autonomous job
async function createJob(userId, taskId, task) {
  const sanitizedTask = sanitizeTask(task);
  const jobData = {
    job_id: taskId,
    user_id: userId,
    task: sanitizedTask,
    timestamp: new Date().toISOString(),
    branch: `job-${taskId}-${Date.now()}`
  };

  try {
    // Create job branch
    await octokit.rest.git.createRef({
      owner: process.env.GITHUB_OWNER || 'your-username',
      repo: process.env.GITHUB_REPO || 'autonomous-bot',
      ref: `refs/heads/${jobData.branch}`,
      sha: (await octokit.rest.git.getRef({
        owner: process.env.GITHUB_OWNER || 'your-username',
        repo: process.env.GITHUB_REPO || 'autonomous-bot',
        ref: 'heads/main'
      })).data.object.sha
    });

    // Trigger GitHub Actions job
    await octokit.rest.repos.createDispatchEvent({
      owner: process.env.GITHUB_OWNER || 'your-username',
      repo: process.env.GITHUB_REPO || 'autonomous-bot',
      event_type: 'job_created',
      client_payload: jobData
    });

    console.log(`Job ${taskId} created for user ${userId}`);
    return jobData;

  } catch (error) {
    console.error('Error creating job:', error);
    throw error;
  }
}

// Generate unique job ID
function generateJobId() {
  return `job-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// Handle Telegram messages
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const task = msg.text;

  console.log(`Message from ${userId}: ${task}`);

  // Security check
  if (!isUserAllowed(userId)) {
    await bot.sendMessage(chatId, '⚠️ You are not authorized to use this bot.');
    return;
  }

  // Skip commands
  if (task.startsWith('/')) {
    return;
  }

  // Create and dispatch job
  const jobId = generateJobId();
  
  try {
    const jobData = await createJob(userId, jobId, task);
    
    await bot.sendMessage(
      chatId, 
      `🤖 Job created!\n\n🎯 Task: ${task}\n📋 Job ID: ${jobId}\n⏰ Started at: ${new Date().toLocaleString()}\n\nI'll notify you when it's completed!`
    );

  } catch (error) {
    await bot.sendMessage(
      chatId,
      `❌ Failed to create job: ${error.message}\n\nPlease try again later.`
    );
  }
});

// Handle commands
bot.onText(/\/start/, async (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;

  if (!isUserAllowed(userId)) {
    await bot.sendMessage(chatId, '⚠️ Access denied.');
    return;
  }

  await bot.sendMessage(
    chatId,
    `🤖 Welcome to the Autonomous Bot!\n\n` +
    `I'm an AI agent that can help you with various tasks.\n\n` +
    `Just send me any task and I'll execute it autonomously!\n\n` +
    `Examples:\n• "Create a simple Python script to..."` +
    `• "Write a blog post about..."` +
    `• "Fix the bug in the function..."` +
    `• "Add a new feature to..."` +
    `\n\nReady to work! What would you like me to do?`
  );
});

bot.onText(/\/status/, async (msg) => {
  const chatId = msg.chat.id;
  
  try {
    const workflows = await octokit.rest.actions.listRepoWorkflows({
      owner: process.env.GITHUB_OWNER || 'your-username',
      repo: process.env.GITHUB_REPO || 'autonomous-bot'
    });

    let status = '📊 *Bot Status*\n\n';
    
    for (const workflow of workflows.data.workflows) {
      const runs = await octokit.rest.actions.listWorkflowRuns({
        owner: process.env.GITHUB_OWNER || 'your-username',
        repo: process.env.GITHUB_REPO || 'autonomous-bot',
        workflow_id: workflow.id,
        per_page: 1
      });

      const latestRun = runs.data.workflow_runs[0];
      const statusEmoji = latestRun.conclusion === 'success' ? '✅' : latestRun.conclusion === 'failure' ? '❌' : '⏳';
      
      status += `${statusEmoji} *${workflow.name}*\n   Status: ${latestRun.status}\n\n`;
    }

    await bot.sendMessage(chatId, status, { parse_mode: 'Markdown' });

  } catch (error) {
    await bot.sendMessage(chatId, `❌ Error checking status: ${error.message}`);
  }
});

// Express server for webhooks
app.use(bodyParser.json());

// GitHub webhook handler
app.post('/webhook', (req, res) => {
  console.log('Received webhook:', req.body);
  
  // Handle different webhook events
  if (req.headers['x-github-event']) {
    const event = req.headers['x-github-event'];
    console.log(`GitHub event: ${event}`);
  }
  
  res.status(200).send('OK');
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    allowed_users: ALLOWED_USERS.length
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Event handler running on port ${PORT}`);
  console.log(`📱 Telegram bot initialized`);
  console.log(`🔐 Security: ${ALLOWED_USERS.length} authorized users`);
  
  // Test connection
  bot.getMe().then(botInfo => {
    console.log(`🤖 Connected to Telegram bot: @${botInfo.username}`);
  });
});

module.exports = app;