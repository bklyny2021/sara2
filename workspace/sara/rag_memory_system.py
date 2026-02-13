#!/usr/bin/env python3
# 🧠 RAG MEMORY SYSTEM for Sara

import os
import hashlib
import json
from pathlib import Path
from datetime import datetime

class RAGMemorySystem:
    """Retrieval-Augmented Generation Memory System for Sara"""
    
    def __init__(self, knowledge_base, memory_file):
        self.knowledge_base = Path(knowledge_base)
        self.memory_file = Path(memory_file)
        self.vector_store = {}
        self.processed_files = set()
        
        # Initialize directories
        os.makedirs(self.knowledge_base, exist_ok=True)
        os.makedirs(self.knowledge_base / "documents", exist_ok=True)
        os.makedirs(self.knowledge_base / "transcripts", exist_ok=True)
        os.makedirs(self.knowledge_base / "pdfs", exist_ok=True)
        
    def load_rag_memory(self):
        """Load existing RAG memory"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse vector store from memory file
                self.parse_vector_store(content)
        print("📚 RAG Memory loaded")
        
    def parse_vector_store(self, content):
        """Parse vector store from memory markdown"""
        # Simple implementation - extract key info
        lines = content.split('\n')
        current_chunk = None
        for line in lines:
            if line.startswith('## 📄'):
                current_chunk = line
                self.vector_store[line] = []
            elif current_chunk and line.strip():
                self.vector_store[current_chunk].append(line.strip())
                
    def scan_and_process_files(self):
        """Scan knowledge base for new files"""
        print("🔍 Scanning for new files...")
        
        # Process PDFs
        self.process_directory("pdfs", self.extract_text_from_pdf)
        
        # Process documents
        self.process_directory("documents", self.extract_text_from_document)
        
        # Process transcripts
        self.process_directory("transcripts", self.extract_text_from_transcript)
        
        print(f"📚 Processed {len(self.processed_files)} files")
        
    def process_directory(self, dir_name, extract_func):
        """Process all files in a directory"""
        dir_path = self.knowledge_base / dir_name
        if not dir_path.exists():
            return
            
        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.md', '.vtt']:
                file_hash = self.calculate_file_hash(file_path)
                if file_hash not in self.processed_files:
                    try:
                        content = extract_func(file_path)
                        self.add_to_vector_store(file_path, content)
                        self.processed_files.add(file_hash)
                        print(f"📄 Processed: {file_path.name}")
                    except Exception as e:
                        print(f"❌ Error processing {file_path}: {e}")
    
    def calculate_file_hash(self, file_path):
        """Calculate file hash for change detection"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            return text
        except ImportError:
            print("❌ PyMuPDF not installed. Install with: pip install PyMuPDF")
            return ""
    
    def extract_text_from_document(self, file_path):
        """Extract text from text documents"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def extract_text_from_transcript(self, file_path):
        """Extract text from transcript files"""
        content = self.extract_text_from_document(file_path)
        # Clean transcript formatting
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            # Remove timestamp and speaker info
            line = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n', '', line)
            line = re.sub(r'<v Speaker="[^"]*">', '', line)
            line = re.sub(r'</v>', '', line)
            if line.strip():
                clean_lines.append(line.strip())
        return '\n'.join(clean_lines)
    
    def add_to_vector_store(self, file_path, content):
        """Add content to vector store"""
        # Simple chunking by paragraphs
        chunks = self.chunk_text(content, 1000)  # 1000 character chunks
        file_key = f"## 📄 {file_path.name}"
        self.vector_store[file_key] = chunks
        
        # Update memory file
        self.update_memory_file(file_path, content)
    
    def chunk_text(self, text, max_length):
        """Split text into manageable chunks"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph + "\n\n") <= max_length:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def update_memory_file(self, file_path, content):
        """Update the memory file with new content"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Append to memory file
        with open(self.memory_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## 📄 {file_path.name}\n")
            f.write(f"**Added:** {timestamp}\n")
            f.write(f"**Type:** {file_path.suffix.upper()}\n")
            f.write(f"**Size:** {len(content)} characters\n\n")
            
            # Add summary of content
            summary = content[:500] + "..." if len(content) > 500 else content
            f.write(f"**Content Preview:**\n```\n{summary}\n```\n\n")
    
    def search_knowledge(self, query, top_k=3):
        """Search knowledge base for relevant information"""
        results = []
        query_lower = query.lower()
        
        for file_key, chunks in self.vector_store.items():
            for i, chunk in enumerate(chunks):
                # Simple relevance scoring based on keyword overlap
                relevance = self.calculate_relevance(query_lower, chunk.lower())
                if relevance > 0:
                    results.append({
                        'file': file_key,
                        'chunk_index': i,
                        'content': chunk,
                        'relevance': relevance
                    })
        
        # Sort by relevance and return top_k
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:top_k]
    
    def calculate_relevance(self, query, content):
        """Simple relevance scoring"""
        query_words = set(query.split())
        content_words = set(content.split())
        
        # Calculate overlap
        overlap = len(query_words.intersection(content_words))
        
        # Normalize by content length
        normalized_overlap = overlap / len(content_words) if content_words else 0
        
        return normalized_overlap
    
    def add_new_knowledge(self, content, source_type="conversation"):
        """Add new knowledge from conversations"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.memory_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## 📝 Conversation Knowledge\n")
            f.write(f"**Added:** {timestamp}\n")
            f.write(f"**Type:** {source_type}\n\n")
            f.write(f"**Content:**\n{content}\n\n")
            
            # Also add to vector store
            file_key = f"## 📝 Conversation {timestamp}"
            if file_key not in self.vector_store:
                self.vector_store[file_key] = []
            self.vector_store[file_key].extend(self.chunk_text(content, 1000))