#!/bin/bash
# Test Sara's actual system access capability
echo "Step 1: Check current cron jobs"
crontab -l

echo ""
echo "Step 2: Add test cron job"
(crontab -l 2>/dev/null; echo "* * * * * echo 'Test cron job executed at' \$(date) >> /tmp/test_cron.log") | crontab -

echo ""
echo "Step 3: Verify cron job added"
crontab -l

echo ""
echo "Step 4: Wait 2 minutes for cron to execute"
echo "Waiting..."
sleep 120

echo ""
echo "Step 5: Check if cron job executed"
if [ -f /tmp/test_cron.log ]; then
    echo "✅ SUCCESS: Cron job executed!"
    echo "Log file contents:"
    cat /tmp/test_cron.log
else
    echo "❌ FAILED: No cron execution detected"
fi

echo ""
echo "Step 6: Clean up - Remove test cron job"
crontab -l | grep -v "test_cron.log" | crontab -

echo ""
echo "Step 7: Clean up log file"
rm -f /tmp/test_cron.log

echo ""
echo "Step 8: Verify cleanup"
crontab -l
if [ ! -f /tmp/test_cron.log ]; then
    echo "✅ SUCCESS: Cleanup complete"
    echo "🎯 TEST COMPLETE: System access confirmed"
else
    echo "❌ FAILED: Cleanup incomplete"
fi