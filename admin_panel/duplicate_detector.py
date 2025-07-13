"""
Optimized duplicate detection system for large question datasets.
Handles 50,000+ questions efficiently using advanced algorithms.
"""

import re
import hashlib
from collections import defaultdict
from difflib import SequenceMatcher
from django.db import models
from django.core.cache import cache
from content.models import Question
import time


class OptimizedDuplicateDetector:
    """
    High-performance duplicate detection system optimized for large datasets.
    Uses text hashing, chunking, and smart filtering to handle 50,000+ questions.
    """
    
    def __init__(self, similarity_threshold=0.95, chunk_size=1000):
        self.similarity_threshold = similarity_threshold
        self.chunk_size = chunk_size
        self.processed_hashes = set()
        self.text_cache = {}
        
    def clean_and_hash_text(self, text):
        """
        Clean text and create multiple hash signatures for fast comparison.
        Returns tuple of (cleaned_text, word_hash, char_hash, length_bucket)
        """
        if text in self.text_cache:
            return self.text_cache[text]
            
        # Clean text
        cleaned = re.sub(r'<[^>]+>', '', text)  # Remove HTML
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
        cleaned = re.sub(r'[^\w\s\?\!\.\,\;\:]', '', cleaned)  # Remove special chars
        cleaned = cleaned.strip().lower()
        
        # Create multiple hash signatures for fast filtering
        words = cleaned.split()
        word_set = set(words)
        
        # Word-based hash (order independent)
        word_hash = hashlib.md5(''.join(sorted(word_set)).encode()).hexdigest()[:16]
        
        # Character-based hash (for typos)
        char_hash = hashlib.md5(''.join(sorted(cleaned.replace(' ', ''))).encode()).hexdigest()[:16]
        
        # Length bucket for quick filtering
        length_bucket = len(cleaned) // 10  # Group by length ranges
        
        result = (cleaned, word_hash, char_hash, length_bucket)
        self.text_cache[text] = result
        return result
    
    def find_duplicates_optimized(self, questions_queryset, progress_callback=None):
        """
        Optimized duplicate detection using multi-stage filtering.
        
        Stage 1: Hash-based exact matches
        Stage 2: Length and word-based filtering  
        Stage 3: Similarity calculation only for candidates
        """
        start_time = time.time()
        
        # Get questions with optimized query
        questions = list(questions_queryset.values(
            'id', 'question_text', 'created_at', 'topic__title',
            'topic__class_level__name', 'topic__class_level__subject__name'
        ).order_by('created_at'))
        
        total_questions = len(questions)
        if total_questions == 0:
            return []
            
        print(f"Processing {total_questions} questions for duplicates...")
        
        # Stage 1: Create hash index for fast lookups
        hash_groups = defaultdict(list)
        processed_questions = []
        
        for i, question in enumerate(questions):
            if progress_callback and i % 100 == 0:
                progress_callback(f"Preprocessing questions... {i}/{total_questions}", (i / total_questions) * 30)
                
            cleaned, word_hash, char_hash, length_bucket = self.clean_and_hash_text(question['question_text'])
            
            processed_questions.append({
                **question,
                'cleaned_text': cleaned,
                'word_hash': word_hash,
                'char_hash': char_hash,
                'length_bucket': length_bucket,
                'word_count': len(cleaned.split())
            })
            
            # Group by word hash for exact matches
            hash_groups[word_hash].append(i)
        
        # Stage 2: Find duplicate groups
        duplicate_groups = []
        processed_indices = set()
        
        # Process hash groups (exact word matches)
        for word_hash, indices in hash_groups.items():
            if len(indices) > 1:
                group = []
                for idx in indices:
                    if idx not in processed_indices:
                        group.append(processed_questions[idx])
                        processed_indices.add(idx)
                
                if len(group) > 1:
                    # Sort by creation date (oldest first)
                    group.sort(key=lambda x: x['created_at'])
                    duplicate_groups.append(group)
        
        # Stage 3: Similarity-based detection for remaining questions
        remaining_questions = [q for i, q in enumerate(processed_questions) if i not in processed_indices]
        
        if remaining_questions:
            similarity_groups = self._find_similarity_groups(remaining_questions, progress_callback, 30, 90)
            duplicate_groups.extend(similarity_groups)
        
        if progress_callback:
            progress_callback("Finalizing results...", 95)
        
        # Format results
        formatted_groups = []
        for group in duplicate_groups:
            if len(group) > 1:
                formatted_groups.append({
                    'group_id': str(group[0]['id']),
                    'questions': group,
                    'count': len(group)
                })
        
        # Sort by count (most duplicates first)
        formatted_groups.sort(key=lambda x: x['count'], reverse=True)
        
        end_time = time.time()
        print(f"Duplicate detection completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(formatted_groups)} duplicate groups")
        
        if progress_callback:
            progress_callback("Complete!", 100)
            
        return formatted_groups
    
    def _find_similarity_groups(self, questions, progress_callback, start_progress, end_progress):
        """
        Find similarity groups using optimized comparison.
        Only compares questions with similar characteristics.
        """
        groups = []
        processed = set()
        total = len(questions)
        
        # Group by length bucket and word count for faster comparison
        length_groups = defaultdict(list)
        for i, q in enumerate(questions):
            length_groups[(q['length_bucket'], q['word_count'])].append((i, q))
        
        current_progress = start_progress
        progress_step = (end_progress - start_progress) / max(len(length_groups), 1)
        
        for group_key, candidates in length_groups.items():
            if len(candidates) < 2:
                continue
                
            # Compare within this length/word group
            for i, (idx1, q1) in enumerate(candidates):
                if idx1 in processed:
                    continue
                    
                group = [q1]
                processed.add(idx1)
                
                for j, (idx2, q2) in enumerate(candidates[i+1:], i+1):
                    if idx2 in processed:
                        continue
                        
                    # Quick pre-filter: check character hash similarity
                    if q1['char_hash'] == q2['char_hash']:
                        group.append(q2)
                        processed.add(idx2)
                    else:
                        # Calculate actual similarity only if needed
                        similarity = SequenceMatcher(None, q1['cleaned_text'], q2['cleaned_text']).ratio()
                        if similarity >= self.similarity_threshold:
                            group.append(q2)
                            processed.add(idx2)
                
                if len(group) > 1:
                    groups.append(group)
            
            current_progress += progress_step
            if progress_callback:
                progress_callback(f"Analyzing similarities... {len(groups)} groups found", current_progress)
        
        return groups


class DuplicateDetector:
    """
    Legacy duplicate detector - kept for compatibility.
    Use OptimizedDuplicateDetector for better performance.
    """
    
    def __init__(self):
        self.similarity_threshold = 0.95
    
    def find_duplicates(self, questions, similarity_threshold=0.95):
        """Legacy method - redirects to optimized version"""
        detector = OptimizedDuplicateDetector(similarity_threshold)
        return detector.find_duplicates_optimized(questions)
