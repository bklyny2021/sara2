#!/usr/bin/env python3
# 🧠 ENHANCED RAG MEMORY SYSTEM - Persistent Memory for Agents

import os
import hashlib
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import re

class EnhancedRAGMemorySystem:
    """Enhanced RAG Memory System with Persistent Database"""
    
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.db_file = self.workspace / "memory" / "agent_memory.db"
        self.knowledge_base = self.workspace / "knowledge"
        self.conversation_log = self.workspace / "memory" / "conversation_history.db"
        
        # Initialize directories
        os.makedirs(self.workspace / "memory", exist_ok=True)
        os.makedirs(self.knowledge_base, exist_ok=True)
        os.makedirs(self.knowledge_base / "documents", exist_ok=True)
        os.makedirs(self.knowledge_base / "transcripts", exist_ok=True)
        os.makedirs(self.knowledge_base / "pdfs", exist_ok=True)
        
        # Initialize database
        self.init_database()
        self.init_conversation_db()
        
    def init_database(self):
        """Initialize SQLite database for persistent memory"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT,
                content TEXT,
                content_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                importance REAL DEFAULT 1.0,
                tags TEXT,
                source_file TEXT,
                chunk_id INTEGER
            )
        ''')
        
        # Create embeddings table (simplified - using text similarity)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER,
                chunk_text TEXT,
                keywords TEXT,
                FOREIGN KEY (memory_id) REFERENCES memory (id)
            )
        ''')
        
        # Create conversation contexts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                agent_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                topic_extracted TEXT,
                context_score REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("🧠 Enhanced RAG Database initialized")
        
    def init_conversation_db(self):
        """Initialize conversation history database"""
        conn = sqlite3.connect(self.conversation_log)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE,
                summary TEXT,
                key_topics TEXT,
                important_events TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                session_type TEXT,
                participants TEXT,
                content TEXT,
                important BOOLEAN DEFAULT 0,
                tags TEXT,
                FOREIGN KEY (date) REFERENCES daily_memories (date)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_agent_memory(self, agent_name):
        """Load all memories for a specific agent"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT content, Content_type, timestamp, importance, tags
            FROM memory 
            WHERE agent_name = ? OR agent_name = 'ALL'
            ORDER BY timestamp DESC
        ''', (agent_name,))
        
        memories = cursor.fetchall()
        conn.close()
        
        print(f"📚 Loaded {len(memories)} memories for {agent_name}")
        return memories
    
    def add_conversation(self, session_id, user_message, agent_response, agent_name):
        """Add conversation to persistent memory"""
        conn = sqlite3.connect(self.conversation_log)
        cursor = conn.cursor()
        
        # Extract topics and context
        topics = self.extract_topics(user_message + " " + agent_response)
        context_score = self.calculate_context_importance(user_message, agent_response)
        
        cursor.execute('''
            INSERT INTO conversations 
            (date, time, session_type, participants, content, important, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d'),
            datetime.now().strftime('%H:%M:%S'),
            'agent_chat',
            f'user,{agent_name}',
            f"USER: {user_message}\nAGENT: {agent_response}",
            context_score > 0.7,
            ','.join(topics)
        ))
        
        conn.commit()
        conn.close()
        
    def add_memory_to_agent(self, agent_name, content, content_type="conversation", importance=1.0, tags=""):
        """Add memory to agent's knowledge base"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memory 
            (agent_name, content, content_type, importance, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (agent_name, content, content_type, importance, tags))
        
        memory_id = cursor.lastrowid
        
        # Add chunks for better retrieval
        chunks = self.chunk_text(content, 500)
        for chunk in chunks:
            keywords = self.extract_keywords(chunk)
            cursor.execute('''
                INSERT INTO embeddings 
                (memory_id, chunk_text, keywords)
                VALUES (?, ?, ?)
            ''', (memory_id, chunk, ','.join(keywords)))
        
        conn.commit()
        conn.close()
        print(f"🧹 Added memory to {agent_name}: {len(chunks)} chunks")
        
    def search_agent_memory(self, agent_name, query, top_k=5):
        """Search agent's memory for relevant information"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        query_lower = query.lower()
        query_terms = query_lower.split()
        
        # Simple text-based search on embeddings
        cursor.execute('''
            SELECT m.content, m.content_type, m.timestamp, e.chunk_text, e.keywords, m.importance
            FROM memory m
            JOIN embeddings e ON m.id = e.memory_id
            WHERE m.agent_name = ? OR m.agent_name = 'ALL'
            ORDER BY m.importance DESC, m.timestamp DESC
        ''', (agent_name,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Score and rank results
        scored_results = []
        for content, content_type, timestamp, chunk, keywords, importance in results:
            relevance = self.calculate_relevance(query_lower, chunk.lower(), keywords)
            if relevance > 0.1:  # Minimum relevance threshold
                scored_results.append({
                    'content': content,
                    'content_type': content_type,
                    'timestamp': timestamp,
                    'chunk': chunk,
                    'relevance': relevance,
                    'importance': importance
                })
        
        # Sort by combined relevance and importance
        scored_results.sort(key=lambda x: (x['relevance'] * x['importance']), reverse=True)
        
        return scored_results[:top_k]
    
    def get_agent_context_summary(self, agent_name):
        """Get context summary for agent from all memories"""
        conn = sqlite3.connect(self.conversation_log)
        cursor = conn.cursor()
        
        # Get recent important conversations
        cursor.execute('''
            SELECT content, tags, important_events
            FROM daily_memories dm
            WHERE dm.date >= date('now', '-30 days')
            ORDER BY dm.created_at DESC
            LIMIT 10
        ''')
        
        summaries = cursor.fetchall()
        conn.close()
        
        context = f"🧠 MEMORY CONTEXT FOR {agent_name.upper()}\\n"
        context += "📅 Recent important conversations:\\n"
        
        for content, tags, events in summaries:
            context += f"• {content[:100]}...\\n"
            if events:
                context += f"  Events: {events}\\n"
        
        return context
    
    def extract_topics(self, text):
        """Extract main topics from text"""
        # Simple keyword extraction
        keywords = []
        
        # Important keywords for agent conversations
        important_words = [
            'agent', 'memory', 'rag', 'voice', 'speech', 'recognition',
            'github', 'upload', 'authentication', 'ssh', 'token',
            'system', 'setup', 'configuration', 'error', 'fix',
            'workflow', 'process', 'document', 'file', 'project'
        ]
        
        text_lower = text.lower()
        for word in important_words:
            if word in text_lower:
                keywords.append(word)
        
        return keywords
    
    def calculate_context_importance(self, user_msg, agent_response):
        """Calculate how important this conversation is"""
        text = (user_msg + " " + agent_response).lower()
        
        # High importance indicators
        high_importance = ['error', 'problem', 'issue', 'fix', 'important', 'urgent', 'auth', 'github', 'ssh', 'token']
        medium_importance = ['setup', 'config', 'system', 'status', 'check']
        
        score = 0.5  # Base score
        
        for word in high_importance:
            if word in text:
                score += 0.3
                
        for word in medium_importance:
            if word in text:
                score += 0.15
        
        return min(score, 1.0)
    
    def extract_keywords(self, text):
        """Extract keywords from chunk"""
        words = text.lower().split()
        # Filter out common words and return meaningful keywords
        keywords = [word for word in words if len(word) > 3 and word not in ['the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'have', 'will']]
        return list(set(keywords))[:10]  # Return unique keywords, max 10
    
    def calculate_relevance(self, query, chunk, keywords_str):
        """Calculate relevance score"""
        query_words = set(query.split())
        keyword_list = keywords_str.split(',') if keywords_str else []
        keywords = set([kw.strip().lower() for kw in keyword_list])
        
        chunk_words = set(chunk.split())
        
        # Score based on exact matches, keyword matches, and word overlap
        exact_matches = len(query_words.intersection(chunk_words))
        keyword_matches = len(query_words.intersection(keywords))
        word_overlap = len(query_words.intersection(chunk_words)) / max(len(query_words), 1)
        
        relevance = (exact_matches * 0.5 + keyword_matches * 0.3 + word_overlap * 0.2) / len(query_words)
        
        return relevance
    
    def chunk_text(self, text, max_length):
        """Split text into manageable chunks"""
        if len(text) <= max_length:
            return [text]
            
        paragraphs = text.split('\\n\\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) <= max_length:
                current_chunk += paragraph + "\\n\\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\\n\\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_memory_statistics(self):
        """Get statistics about stored memories"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Total memories
        cursor.execute('SELECT COUNT(*) FROM memory')
        total_memories = cursor.fetchone()[0]
        
        # Memories by agent
        cursor.execute('SELECT agent_name, COUNT(*) FROM memory GROUP BY agent_name')
        by_agent = cursor.fetchall()
        
        # Recent conversations
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE date >= date("now", "-7 days")')
        recent_convs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_memories': total_memories,
            'by_agent': dict(by_agent),
            'recent_conversations': recent_convs
        }

# Usage example for agent spawn
def initialize_agent_with_memory(agent_name, workspace_path):
    """Initialize agent with its full memory context"""
    memory_system = EnhancedRAGMemorySystem(workspace_path)
    
    # Load all memories for this agent
    memories = memory_system.load_agent_memory(agent_name)
    context = memory_system.get_agent_context_summary(agent_name)
    
    # Get recent memories for immediate context
    recent_memories = memory_system.search_agent_memory(agent_name, "", top_k=10)
    
    context_summary = f"\\n=== {agent_name.upper()} MEMORY CONTEXT ===\\n"
    context_summary += f"Total memories loaded: {len(memories)}\\n\\n"
    
    if recent_memories:
        context_summary += "RECENT IMPORTANT MEMORIES:\\n"
        for i, mem in enumerate(recent_memories[:5]):
            context_summary += f"{i+1}. {mem['chunk'][:100]}... [{mem['timestamp']}][Importance: {mem['importance']}]\\n"
    
    context_summary += f"\\n=== CONTEXT COMPLETE ===\\n"
    
    return memory_system, context_summary