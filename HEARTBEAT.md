# HEARTBEAT.md - Periodic Checks

_Things to check periodically. The agent reads this when it receives a heartbeat._

## Current Tasks

### Hourly (or ~4x/day)

1. **Check Cron Jobs Status**
   - Run: `cron list` 
   - Ensure jobs are running
   - Report any errors

2. **Memory Maintenance**
   - Review recent memory files
   - Update MEMORY.md with significant learnings
   - Archive old daily files if needed

3. **Session Health**
   - List active sessions
   - Check for stuck/failed jobs
   - Report unusual activity

### Daily

1. **Security Review**
   - Check security-status.log
   - Verify firewall/SSH status
   - Update if threats detected

2. **Code & Documentation**
   - Review BUILD_LOG.json progress
   - Check for uncommitted changes
   - Ensure documentation is current

### Weekly

1. **Growth Analysis**
   - Review MEMORY.md for outdated info
   - Identify new expansion opportunities
   - Plan capability development

2. **System Optimization**
   - Review cron schedules
   - Check for performance issues
   - Optimize where possible

## When to Speak Up

**Alert Boo when:**
- Cron job fails repeatedly
- Security issue detected
- Critical service down
- Important calendar event <2h away
- You've been silent >8h

**Stay quiet (HEARTBEAT_OK) when:**
- Late night (23:00-08:00) unless urgent
- Nothing new since last check
- Just checked <30 min ago
- Everything is nominal

## Proactive Work Allowed

Without asking, you can:
- Read and organize memory files
- Update documentation
- Commit/push changes
- Review logs
- Fix obvious issues

## State Tracking

Track checks in `/home/sarabot/.openclaw/workspace/memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "cron": 0,
    "memory": 0,
    "security": 0
  }
}
```

---

_Last updated: Check when modified_
