#!/usr/bin/env python3
# 🧠 MEMORY-AWARE AGENT SPAWNER

import os
import sys
from enhanced_rag_memory_system import EnhancedRAGMemorySystem, initialize_agent_with_memory

def spawn_agent_with_memory(agent_name, workspace_path=None):
    """Spawn an agent with its complete memory context loaded"""
    
    if not workspace_path:
        workspace_path = os.path.dirname(os.path.abspath(__file__))
    
    print(f"🚀 Spawning {agent_name} with full RAG memory...")
    
    # Initialize and load memory system
    memory_system = EnhancedRAGMemorySystem(workspace_path)
    
    # Get agent's complete context
    context_summary = memory_system.get_agent_context_summary(agent_name)
    recent_memories = memory_system.search_agent_memory(agent_name, "", top_k=10)
    
    # Create memory prompt
    memory_prompt = f"""
=== {agent_name.upper()} - MEMORY LOADED ===

📚 TOTAL MEMORY CONTEXT:
{context_summary}

🧠 RECENT IMPORTANT MEMORIES:
"""
    
    for i, mem in enumerate(recent_memories[:5]):
        memory_prompt += f"{i+1}. {mem['chunk'][:120]}... [{mem['timestamp']}][Importance: {mem['importance']}]\\n"
    
    memory_prompt += f"""
=== MEMORY SYSTEM ACTIVE ===
✅ All conversations since day one stored
✅ Automatic context retrieval enabled  
✅ Continuous learning from interactions
✅ Never forget important details

You now have complete memory awareness. Every conversation will be stored and referenced in future interactions.
=============================================
"""
    
    # Add this spawn event to memory
    memory_system.add_memory_to_agent(
        agent_name, 
        f"Agent {agent_name} spawned with full RAG memory system. Memory context loaded: {len(context_summary)} characters, {len(recent_memories)} recent memories.",
        content_type="system_event",
        importance=1.0,
        tags="spawn,memory,rag,context"
    )
    
    stats = memory_system.get_memory_statistics()
    
    print(f"🧠 Memory System Status:")
    print(f"   • Total memories: {stats['total_memories']}")
    print(f"   • Recent conversations: {stats['recent_conversations']}")
    print(f"   • Memories for {agent_name}: {stats['by_agent'].get(agent_name, 0)}")
    print(f"   • Context preview: {context_summary[:100]}...")
    print(f"✅ Agent {agent_name} now has FULL MEMORY AWARENESS")
    
    return memory_system, memory_prompt

if __name__ == "__main__":
    agent_name = sys.argv[1] if len(sys.argv) > 1 else "sara"
    workspace_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    memory_system, context = spawn_agent_with_memory(agent_name, workspace_path)
    print(f"\\n🧠 Memory Context for {agent_name}:")
    print(context[:500] + "..." if len(context) > 500 else context)