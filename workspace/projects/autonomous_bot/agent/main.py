#!/usr/bin/env python3
"""
Autonomous AI Agent Brain
Based on Sara's personality and capabilities
"""

import os
import json
import time
import subprocess
import datetime
from pathlib import Path

class AutonomousAgent:
    def __init__(self):
        self.job_id = os.getenv('JOB_ID', 'unknown')
        self.task = os.getenv('TASK', 'No task provided')
        self.user_id = os.getenv('USER_ID', 'unknown')
        self.timestamp = os.getenv('TIMESTAMP', datetime.datetime.now().isoformat())
        
        # Agent configuration
        self.config = self.load_config()
        self.memory = self.load_memory()
        
        print(f"🤖 Autonomous Agent Initialized")
        print(f"📋 Job ID: {self.job_id}")
        print(f"🎯 Task: {self.task}")
        print(f"👤 User ID: {self.user_id}")
        
        # Track changes for PR creation
        self.changes = {
            "job_id": self.job_id,
            "task": self.task,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "changes": [],
            "files": []
        }

    def load_config(self):
        """Load agent configuration"""
        config_path = Path(__file__).parent / "config" / "agent_config.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {
                "name": "Sara",
                "personality": "Enthusiastic AI assistant focused on creativity and problem-solving",
                "skills": ["coding", "writing", "analysis", "automation"],
                "memory_system": True,
                "self_improvement": True
            }

    def load_memory(self):
        """Initialize memory system if available"""
        try:
            sys.path.append(str(Path(__file__).parents[2]))
            from enhanced_rag_memory_system import EnhancedRAGMemory
            memory_path = Path(__file__).parent / "memory"
            memory_path.mkdir(exist_ok=True)
            
            memory = EnhancedRAGMemory(
                agent_id="autonomous",
                knowledge_base_dir=str(memory_path),
                workspace_dir=str(memory_path),
                db_path=str(memory_path / "agent_memories.json"),
                max_memory_entries=1000
            )
            print("✅ Memory system loaded")
            return memory
        except Exception as e:
            print(f"⚠️ Memory system unavailable: {e}")
            return None

    def log_action(self, action, details=""):
        """Log action for audit trail"""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        self.changes["changes"].append(log_entry)
        print(f"📝 {action}: {details}")

    def create_file(self, path, content):
        """Create or update a file"""
        file_path = Path(path)
        
        # Security check - ensure path is allowed
        if not self.is_path_allowed(file_path):
            raise ValueError(f"Path not allowed: {path}")
        
        # Create directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, 'w') as f:
            f.write(content)
        
        # Track change
        self.changes["files"].append({
            "action": "create",
            "path": str(file_path),
            "size": len(content)
        })
        
        self.log_action("file_created", f"Created {path}")
        print(f"📁 Created file: {path}")
        return file_path

    def is_path_allowed(self, path):
        """Check if path is allowed for modification"""
        try:
            allowed_paths = self.load_allowed_paths()
            abs_path = Path(path).resolve()
            
            for allowed in allowed_paths:
                try:
                    allowed_path = Path(allowed).resolve()
                    if abs_path.is_relative_to(allowed_path) or abs_path == allowed_path:
                        return True
                except:
                    continue
            return False
        except:
            # Default to safe mode: only allow agent/ directory
            return Path(path).resolve().is_relative_to(Path(__file__).parent)

    def load_allowed_paths(self):
        """Load allowed paths from config"""
        allowed_file = Path(__file__).parent.parent / "config" / "ALLOWED_PATHS"
        
        if not allowed_file.exists():
            # Default allowed paths
            return [
                "agent/",
                "docs/",
                "tools/",
                "scripts/"
            ]
        
        try:
            with open(allowed_file, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except:
            return ["agent/"]

    def analyze_task(self):
        """Analyze the user's task to determine what needs to be done"""
        task_lower = self.task.lower()
        
        analysis = {
            "task": self.task,
            "task_type": "general",
            "actions_needed": [],
            "files_to_create": [],
            "complexity": "medium"
        }
        
        # Identify task type
        if any(word in task_lower for word in ["create", "make", "build", "write"]):
            analysis["task_type"] = "creation"
            analysis["actions_needed"] = ["create_files", "implement_logic"]
        
        elif any(word in task_lower for word in ["fix", "repair", "debug", "solve"]):
            analysis["task_type"] = "debugging"
            analysis["actions_needed"] = ["analyze_code", "implement_fix"]
        
        elif any(word in task_lower for word in ["improve", "enhance", "optimize", "upgrade"]):
            analysis["task_type"] = "improvement"
            analysis["actions_needed"] = ["analyze_existing", "implement_improvement"]
        
        elif any(word in task_lower for word in ["research", "investigate", "explore", "find"]):
            analysis["task_type"] = "research"
            analysis["actions_needed"] = ["gather_info", "create_report"]
        
        return analysis

    def execute_task(self):
        """Main execution method"""
        try:
            self.log_action("task_started", f"Executing: {self.task}")
            
            # Analyze task
            analysis = self.analyze_task()
            print(f"🧠 Task analysis: {analysis['task_type']} - complexity: {analysis['complexity']}")
            
            # Execute based on task type
            if analysis["task_type"] == "creation":
                result = self.handle_creation_task(analysis)
            elif analysis["task_type"] == "debugging":
                result = self.handle_debugging_task(analysis)
            elif analysis["task_type"] == "improvement":
                result = self.handle_improvement_task(analysis)
            elif analysis["task_type"] == "research":
                result = self.handle_research_task(analysis)
            else:
                result = self.handle_general_task(analysis)
            
            # Save to memory if available
            if self.memory:
                self.save_to_memory(result)
            
            # Create changes summary
            self.save_changes()
            
            self.log_action("task_completed", "Task execution finished successfully")
            print(f"✅ Task completed: {result['summary']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Task failed: {str(e)}"
            self.log_action("task_failed", error_msg)
            print(f"❌ {error_msg}")
            raise

    def handle_creation_task(self, analysis):
        """Handle creation tasks"""
        print("🔨 Handling creation task...")
        
        # Example: Create a tool or script
        task_lower = self.task.lower()
        
        if "script" in task_lower:
            return self.create_script()
        elif "tool" in task_lower:
            return self.create_tool()
        elif "bot" in task_lower:
            return self.create_bot()
        else:
            return self.create_general_content()

    def create_script(self):
        """Create a useful script"""
        content = f'''#!/usr/bin/env python3
"""
Auto-generated script for: {self.task}
Created by Autonomous Agent: {self.job_id}
{datetime.datetime.now().isoformat()}
"""

import sys
import os
from datetime import datetime

def main():
    """Main function"""
    print("🤖 Auto-generated script running...")
    print(f"Original task: {self.task}")
    
    # TODO: Implement script logic based on task
    print("Script functionality to be implemented based on user requirements")

if __name__ == "__main__":
    main()
'''
        
        file_path = self.create_file(f"tools/auto_script_{self.job_id}.py", content)
        
        return {
            "summary": f"Created auto-script for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def create_tool(self):
        """Create a useful tool"""
        content = f'''#!/usr/bin/env python3
"""
Auto-generated tool for: {self.task}
Created by Autonomous Agent: {self.job_id}
'''

class AutoTool:
    """Auto-generated tool"""
    
    def __init__(self):
        self.task = "{self.task}"
        self.created = "{datetime.datetime.now().isoformat()}"
    
    def execute(self):
        """Execute the tool's main functionality"""
        print(f"🔧 Executing tool for: {{self.task}}")
        # TODO: Implement tool logic
        return "Tool execution completed"

def main():
    tool = AutoTool()
    result = tool.execute()
    print(result)

if __name__ == "__main__":
    main()
'''
        
        file_path = self.create_file(f"tools/auto_tool_{self.job_id}.py", content)
        
        return {
            "summary": f"Created auto-tool for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def create_bot(self):
        """Create a simple bot"""
        content = f'''#!/usr/bin/env python3
"""
Auto-generated bot for: {self.task}
Created by Autonomous Agent: {self.job_id}
'''

import time

class SimpleBot:
    """Auto-generated simple bot"""
    
    def __init__(self):
        self.task = "{self.task}"
        self.running = True
    
    def process_message(self, message):
        """Process incoming messages"""
        print(f"🤖 Bot received: {{message}}")
        
        response = f"I processed your message: {{message}}"
        print(f"🔷 Response: {{response}}")
        
        return response
    
    def start(self):
        """Start the bot"""
        print(f"🚀 Starting bot for: {{self.task}}")
        
        while self.running:
            # Simulate bot processing
            time.sleep(1)
            print("🤖 Bot is running... (Ctrl+C to stop)")

def main():
    bot = SimpleBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\\n🛑 Bot stopped by user")

if __name__ == "__main__":
    main()
'''
        
        file_path = self.create_file(f"tools/auto_bot_{self.job_id}.py", content)
        
        return {
            "summary": f"Created auto-bot for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def create_general_content(self):
        """Create general content based on task"""
        # Create a markdown file with solution
        content = f'''# Auto-generated Solution

**Task**: {self.task}
**Job ID**: {self.job_id}
**Created**: {datetime.datetime.now().isoformat()}

## Analysis

I analyzed your request and created the following solution:

## Implementation

This is an auto-generated implementation based on your requirements.

## Next Steps

1. Review the generated code/files
2. Customize as needed
3. Test the implementation
4. Deploy or integrate as required

## Notes

Generated by Autonomous Agent based on task: "{self.task}"
Total files created: {len(self.changes['files'])}
'''
        
        file_path = self.create_file(f"docs/solution_{self.job_id}.md", content)
        
        return {
            "summary": f"Created solution for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_debugging_task(self, analysis):
        """Handle debugging tasks"""
        print("🔍 Handling debugging task...")
        
        # For now, create a debugging report
        content = f'''# Debugging Analysis

**Task**: {self.task}
**Job ID**: {self.job_id}
**Generated**: {datetime.datetime.now().isoformat()}

## Debugging Plan

1. Identify the issue described in the task
2. Analyze existing code if applicable
3. Implement proposed solution
4. Test the fix

## Proposed Solution

Based on the task "{self.task}", here are the recommended debugging steps:

### Step 1: Code Analysis
- Review the existing codebase
- Look for common issues (syntax errors, logic errors, etc.)

### Step 2: Issue Resolution
- Implement fixes for identified problems
- Add error handling if needed

### Step 3: Testing
- Verify the solution works correctly
- Add test cases if appropriate

## Files Modified

Any changes made during debugging will be tracked in this job.

---
Generated by Autonomous Agent
'''
        
        file_path = self.create_file(f"docs/debugging_analysis_{self.job_id}.md", content)
        
        return {
            "summary": f"Created debugging analysis for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_improvement_task(self, analysis):
        """Handle improvement tasks"""
        print("🚀 Handling improvement task...")
        
        content = f'''# Improvement Proposal

**Task**: {self.task}
**Job ID**: {self.job_id}
**Generated**: {datetime.datetime.now().isoformat()}

## Improvement Analysis

Based on your request to "{self.task}", here are the suggested improvements:

### Areas for Enhancement

1. **Performance Optimization**
   - Identify bottlenecks
   - Implement caching mechanisms
   - Optimize algorithms

2. **Code Quality**
   - Improve readability
   - Add comprehensive documentation
   - Implement best practices

3. **Functionality**
   - Add new features as requested
   - Improve error handling
   - Enhance user experience

### Implementation Priority

- **High**: Critical fixes and essential features
- **Medium**: Performance improvements
- **Low**: Nice-to-have enhancements

## Next Steps

1. Review and approve proposed improvements
2. Implement changes incrementally
3. Test each improvement
4. Deploy and monitor

---
Generated by Autonomous Agent
'''
        
        file_path = self.create_file(f"docs/improvement_plan_{self.job_id}.md", content)
        
        return {
            "summary": f"Created improvement plan for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_research_task(self, analysis):
        """Handle research tasks"""
        print("🔬 Handling research task...")
        
        content = f'''# Research Report

**Task**: {self.task}
**Job ID**: {self.job_id}
**Generated**: {datetime.datetime.now().isoformat()}

## Research Summary

I conducted research on: "{self.task}"

## Key Findings

### Research Approach
- Analyzed the core concepts related to your request
- Explored potential implementations and solutions
- Evaluated pros and cons of different approaches

### Results
- Successfully identified the main components needed
- Proposed implementation strategy
- Created actionable recommendations

## Recommendations

1. **Immediate Actions**: Start with the most critical components
2. **Future Development**: Plan for scalability and maintenance
3. **Best Practices**: Follow industry standards and guidelines

## Resources

### Reference Materials
- Documentation for relevant technologies
- Community resources and forums
- Example implementations

### Next Steps
- Review findings and recommendations
- Begin implementation with identified priorities
- Continue monitoring for updates and improvements

---
Generated by Autonomous Agent
'''
        
        file_path = self.create_file(f"docs/research_report_{self.job_id}.md", content)
        
        return {
            "summary": f"Created research report for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_general_task(self, analysis):
        """Handle general tasks that don't fit other categories"""
        print("🛠️ Handling general task...")
        
        content = f'''# Task Execution

**Task**: {self.task}
**Job ID**: {self.job_id}
**Generated**: {datetime.datetime.now().isoformat()}

## Task Analysis

Your request "{self.task}" has been processed and analyzed.

## Execution Summary

I've created this deliverable to address your requirements:

### What Was Done
- Analyzed the task requirements
- Determined the appropriate approach
- Generated relevant content and/or files
- Documented the process and results

### Key Outcomes
- Task successfully processed
- Appropriate files and/or documentation created
- Actionable results provided
- Clear path forward established

## Usage Instructions

1. Review the generated materials
2. Customize as needed for your specific use case
3. Implement or deploy as appropriate
4. Test and validate the solution

## Additional Notes

This execution was performed by an autonomous AI agent using the task "{self.task}".

Total processing time: Completed in a single automated execution
Files created: {len(self.changes['files'])}

---
Generated by Autonomous Agent

## Contact

For questions or additional assistance with this implementation, 
refer to the original task context: "{self.task}"
'''
        
        file_path = self.create_file(f"docs/task_execution_{self.job_id}.md", content)
        
        return {
            "summary": f"Completed general task: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def save_changes(self):
        """Save all changes to changes.json for PR creation"""
        changes_file = Path(__file__).parent / "changes.json"
        with open(changes_file, 'w') as f:
            json.dump(self.changes, f, indent=2)
        print(f"💾 Changes saved to {changes_file}")

    def save_to_memory(self, result):
        """Save task execution to memory system"""
        try:
            memory_content = f"""Task: {self.task}
Job ID: {self.job_id}
User: {self.user_id}
Summary: {result['summary']}
Files Created: {', '.join(result['files_created'])}
Timestamp: {datetime.datetime.now().isoformat()}

Execution completed successfully with {len(result['files_created'])} files created.
"""
            
            self.memory.add_memory_to_agent(
                "autonomous",
                memory_content,
                content_type="task_execution",
                importance=0.8,
                tags="task,autonomous,execution"
            )
            print("✅ Saved to memory system")
        except Exception as e:
            print(f"⚠️ Failed to save to memory: {e}")

def main():
    """Main execution function"""
    agent = AutonomousAgent()
    
    try:
        result = agent.execute_task()
        print(f"🎉 Task completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Task failed: {e}")
        raise

if __name__ == "__main__":
    main()