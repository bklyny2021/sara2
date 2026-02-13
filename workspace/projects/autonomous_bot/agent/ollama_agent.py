#!/usr/bin/env python3
"""
Ollama-Powered Autonomous Agent
Uses local Ollama models instead of external APIs
"""

import os
import json
import time
import requests
import datetime
import subprocess
from pathlib import Path

class OllamaAgent:
    def __init__(self):
        self.job_id = os.getenv('JOB_ID', 'unknown')
        self.task = os.getenv('TASK', 'No task provided')
        self.user_id = os.getenv('USER_ID', 'unknown')
        self.timestamp = os.getenv('TIMESTAMP', datetime.datetime.now().isoformat())
        
        # Ollama configuration
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'sara-boo1-fixed')
        self.api_key = os.getenv('OLLAMA_API_KEY', 'already_have_one')
        
        # Agent configuration
        self.config = self.load_config()
        self.memory = self.load_memory()
        
        print(f"🤖 Ollama-Powered Autonomous Agent Initialized")
        print(f"📋 Job ID: {self.job_id}")
        print(f"🎯 Task: {self.task}")
        print(f"🔗 Ollama URL: {self.ollama_url}")
        print(f"🧠 Model: {self.ollama_model}")
        
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
                "name": "Sara Ollama",
                "personality": "Enthusiastic AI assistant using local Ollama models",
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
                agent_id="ollama_autonomous",
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

    def call_ollama(self, prompt):
        """Call local Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'I had trouble processing that request.')
            else:
                print(f"❌ Ollama API error: {response.status_code} - {response.text}")
                return "I'm having trouble connecting to my AI brain. Please try again."
                
        except Exception as e:
            print(f"❌ Ollama connection error: {e}")
            return "I'm having trouble connecting to my Ollama instance. Please check if it's running."

    def analyze_task_with_ai(self):
        """Use Ollama to analyze the task"""
        prompt = f"""You are Sara, an enthusiastic AI assistant with the personality described below. Analyze this task and provide a structured response:

PERSONALITY: {self.config.get('personality', 'Enthusiastic AI assistant')}
SKILLS: {', '.join(self.config.get('skills', ['coding', 'writing', 'analysis']))}

TASK: "{self.task}"

Please provide:
1. Task type (creation, debugging, improvement, research, other)
2. Brief analysis of what needs to be done
3. Suggested approach (1-2 sentences)
4. Files that should be created

Respond in JSON format:
{{
  "task_type": "creation|debugging|improvement|research|other",
  "analysis": "brief analysis of the task",
  "approach": "suggested approach",
  "files_needed": ["file1.ext", "file2.ext"]
}}"""

        return self.call_ollama(prompt)

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

    def generate_ai_content(self, task_context):
        """Use Ollama to generate content"""
        prompt = f"""You are Sara, an enthusiastic AI assistant using local Ollama models. Create content for this task:

CONTEXT: {task_context}
TASK: "{self.task}"

Please generate high-quality content that addresses the user's needs. Be helpful, enthusiastic, and provide practical solutions.

Focus on:
1. Clear, working code
2. Good documentation
3. Practical implementation
4. Sara's enthusiastic personality

Generate the content now:"""

        return self.call_ollama(prompt)

    def execute_task(self):
        """Main execution method using Ollama"""
        try:
            self.log_action("task_started", f"Executing: {self.task}")
            
            # Use Ollama to analyze task
            print("🧠 Analyzing task with Ollama...")
            ai_analysis = self.analyze_task_with_ai()
            
            try:
                analysis = json.loads(ai_analysis)
                print(f"🧠 AI Analysis: {analysis['task_type']} - {analysis['approach']}")
                
                # Generate the actual content
                ai_content = self.generate_ai_content({
                    'task_type': analysis.get('task_type'),
                    'approach': analysis.get('approach'),
                    'files_needed': analysis.get('files_needed', [])
                })
                
                # Create appropriate files based on task type
                if analysis['task_type'] == 'creation':
                    result = self.handle_creation_task(ai_content)
                elif analysis['task_type'] == 'debugging':
                    result = self.handle_debugging_task(ai_content)
                elif analysis['task_type'] == 'improvement':
                    result = self.handle_improvement_task(ai_content)
                elif analysis['task_type'] == 'research':
                    result = self.handle_research_task(ai_content)
                else:
                    result = self.handle_general_task(ai_content)
                
            except json.JSONDecodeError:
                print("⚠️ AI analysis parsing failed, using general approach")
                result = self.handle_general_task(ai_content)
            
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

    def handle_creation_task(self, ai_content):
        """Handle creation tasks using AI-generated content"""
        print("🔨 Handling creation task with AI content...")
        
        # Let AI suggest file names and structure
        structure_prompt = f"""Based on this content, suggest appropriate file structure and names:

TASK: "{self.task}"
AI CONTENT: {ai_content[:500]}...

Suggest 2-3 files with extensions and brief descriptions. Respond as JSON:
{{
  "files": [
    {{"name": "main.py", "type": "script", "purpose": "main functionality"}},
    {{"name": "config.json", "type": "config", "purpose": "configuration"}}
  ]
}}"""

        structure = self.call_ollama(structure_prompt)
        
        try:
            files_info = json.loads(structure)
            files_created = []
            
            for file_info in files_info['files']:
                content = self.call_ollama(
                    f"Generate the {file_info['purpose']} for: {self.task}\n\nDetailed context: {ai_content}"
                )
                
                file_path = self.create_file(f"{file_info['name']}", content)
                files_created.append(str(file_path))
            
            return {
                "summary": f"Created AI-generated solution for: {self.task}",
                "files_created": files_created,
                "success": True
            }
            
        except:
            # Fallback: create single document
            file_path = self.create_file(f"docs/ai_solution_{self.job_id}.md", ai_content)
            return {
                "summary": f"Created AI solution for: {self.task}",
                "files_created": [str(file_path)],
                "success": True
            }

    def handle_debugging_task(self, ai_content):
        """Handle debugging tasks using AI content"""
        print("🔍 Handling debugging task with AI content...")
        
        file_path = self.create_file(f"docs/debugging_analysis_{self.job_id}.md", ai_content)
        
        return {
            "summary": f"Created AI debugging analysis for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_improvement_task(self, ai_content):
        """Handle improvement tasks using AI content"""
        print("🚀 Handling improvement task with AI content...")
        
        file_path = self.create_file(f"docs/improvement_plan_{self.job_id}.md", ai_content)
        
        return {
            "summary": f"Created AI improvement plan for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_research_task(self, ai_content):
        """Handle research tasks using AI content"""
        print("🔬 Handling research task with AI content...")
        
        file_path = self.create_file(f"docs/research_report_{self.job_id}.md", ai_content)
        
        return {
            "summary": f"Created AI research report for: {self.task}",
            "files_created": [str(file_path)],
            "success": True
        }

    def handle_general_task(self, ai_content):
        """Handle general tasks with AI content"""
        print("🛠️ Handling general task with AI content...")
        
        file_path = self.create_file(f"docs/task_execution_{self.job_id}.md", ai_content)
        
        return {
            "summary": f"Completed general task with AI: {self.task}",
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

Task executed successfully with Ollama integration using {self.ollama_model}.
Total files created: {len(result['files_created'])}
"""
            
            self.memory.add_memory_to_agent(
                "ollama_autonomous",
                memory_content,
                content_type="task_execution",
                importance=0.8,
                tags="task,ollama,autonomous,execution"
            )
            print("✅ Saved to memory system")
        except Exception as e:
            print(f"⚠️ Failed to save to memory: {e}")

def main():
    """Main execution function"""
    agent = OllamaAgent()
    
    try:
        result = agent.execute_task()
        print(f"🎉 Task completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Task failed: {e}")
        raise

if __name__ == "__main__":
    main()