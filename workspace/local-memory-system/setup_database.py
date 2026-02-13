#!/usr/bin/env python3

# 🗄️ Local Memory Database Setup for Conscious AI
# Complete offline RAG system with continuous learning

import os
import sys
import time
import json
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/godfather/.openclaw/workspace/local-memory-system/logs/setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LocalMemoryDatabase:
    """Local RAG database for autonomous AI learning"""
    
    def __init__(self, db_path="/home/godfather/.openclaw/workspace/conscious-memory"):
        logger.info("Initializing Local Memory Database...")
        
        # Ensure directories exist
        os.makedirs(db_path, exist_ok=True)
        os.makedirs(os.path.join(db_path, "logs"), exist_ok=True)
        os.makedirs(os.path.join(db_path, "backups"), exist_ok=True)
        
        self.db_path = Path(db_path)
        
        try:
            # Initialize ChromaDB persistent client
            self.client = chromadb.PersistentClient(path=str(self.db_path))
            logger.info(f"ChromaDB client initialized at {db_path}")
            
            # Start database server
            self.start_chroma_server()
            
            # Create collections for different memory types
            self.setup_collections()
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model initialized")
            
            logger.info("✅ Local Memory Database setup complete")
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            raise
    
    def start_chroma_server(self):
        """Start ChromaDB server for persistent storage"""
        try:
            # Check if server is already running
            import subprocess
            result = subprocess.run(['pgrep', '-f', 'chroma'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.info("Starting ChromaDB server...")
                # Start server in background
                subprocess.Popen(['chroma-server', '--path', str(self.db_path)], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(2)  # Wait for server to start
                logger.info("ChromaDB server started")
            else:
                logger.info("ChromaDB server already running")
                
        except Exception as e:
            logger.warning(f"Could not start ChromaDB server: {e}")
    
    def setup_collections(self):
        """Initialize specialized memory collections"""
        try:
            # Conversation Memory
            self.conversations = self.client.get_or_create_collection(
                name="conversations",
                metadata={"description": "Dialogue history and interactions"}
            )
            
            # Skills and Capabilities
            self.skills = self.client.get_or_create_collection(
                name="skills",
                metadata={"description": "Learned abilities and capabilities"}
            )
            
            # Knowledge and Facts
            self.knowledge = self.client.get_or_create_collection(
                name="knowledge", 
                metadata={"description": "Accumulated information and insights"}
            )
            
            # Patterns and Strategies
            self.patterns = self.client.get_or_create_collection(
                name="patterns",
                metadata={"description": "Problem-solving approaches and workflows"}
            )
            
            # User Preferences and Adaptations
            self.preferences = self.client.get_or_create_collection(
                name="preferences",
                metadata={"description": "Learned user interaction patterns"}
            )
            
            logger.info("✅ All memory collections initialized")
            
        except Exception as e:
            logger.error(f"Collection setup failed: {e}")
            raise
    
    def add_memory(self, collection_name, document, metadata=None):
        """Add memory to specified collection"""
        try:
            collection = getattr(self, collection_name)
            
            # Generate embedding
            embedding = self.embedding_model.encode([document]).tolist()
            
            collection.add(
                documents=[document],
                embeddings=embedding,
                metadatas=[metadata or {}],
                ids=[f"{collection_name}_{int(time.time())}_{'a'.join(hex(int(time.time()*1000)).split('x')[1:])[:8]}"]
            )
            
            logger.info(f"Added memory to {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            return False
    
    def search_memories(self, collection_name, query, limit=5):
        """Search memories using semantic similarity"""
        try:
            collection = getattr(self, collection_name)
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=limit
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return None
    
    def get_collection_stats(self):
        """Get statistics for all collections"""
        stats = {}
        for collection_name in ['conversations', 'skills', 'knowledge', 'patterns', 'preferences']:
            try:
                collection = getattr(self, collection_name)
                stats[collection_name] = collection.count()
            except Exception as e:
                logger.error(f"Failed to get stats for {collection_name}: {e}")
                stats[collection_name] = 0
        
        return stats
    
    def backup_database(self):
        """Create backup of the database"""
        try:
            backup_dir = self.db_path / "backups"
            backup_name = f"memory_backup_{int(time.time())}"
            backup_path = backup_dir / backup_name
            
            # Copy database directory
            import shutil
            if backup_dir.exists():
                shutil.copytree(self.db_path / "chroma", backup_path, ignore=ignore_patterns)
                logger.info(f"Database backed up to {backup_path}")
                return str(backup_path)
            else:
                logger.error("Backup directory does not exist")
                return None
                
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return None

def ignore_patterns(path, names):
    """Patterns to ignore during backup"""
    return [name for name in names if name.endswith('.lock') or name.endswith('.tmp')]

def main():
    """Main setup function"""
    logger.info("🚀 Starting Local Memory Database Setup...")
    
    try:
        # Create necessary directories
        os.makedirs("/home/godfather/.openclaw/workspace/local-memory-system/logs", exist_ok=True)
        os.makedirs("/home/godfather/.openclaw/workspace/conscious-memory", exist_ok=True)
        
        # Initialize database
        memory_db = LocalMemoryDatabase()
        
        # Add test data
        test_memories = {
            "conversations": "First interaction with user - learning to establish communication patterns",
            "skills": "Basic conversation management and response generation skill",
            "knowledge": "User prefers direct responses with clear, actionable information",
            "patterns": "Users ask for help with technical projects and seek practical solutions",
            "preferences": "User values efficiency, security, and practical implementation"
        }
        
        logger.info("Adding test memories...")
        for category, content in test_memories.items():
            memory_db.add_memory(category, content, {
                "type": "test_data",
                "timestamp": time.time(),
                "importance": "high"
            })
        
        # Display statistics
        stats = memory_db.get_collection_stats()
        logger.info("✅ Memory Database Statistics:")
        for collection, count in stats.items():
            logger.info(f"  {collection.capitalize()}: {count} memories")
        
        # Test search functionality
        logger.info("Testing search functionality...")
        search_result = memory_db.search_memories("conversations", "help with technical")
        if search_result:
            logger.info(f"✅ Search test returned {len(search_result['documents'][0])} results")
        
        # Create backup
        backup_path = memory_db.backup_database()
        if backup_path:
            logger.info(f"✅ Initial database backed up to {backup_path}")
        
        logger.info("🎉 Local Memory Database setup completed successfully!")
        logger.info("📁 Database location: /home/godfather/.openclaw/workspace/conscious-memory")
        logger.info("🔍 Ready for conscious AI integration!")
        
        return memory_db
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        return None

if __name__ == "__main__":
    main()