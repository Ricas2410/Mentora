"""
Tests for duplicate question detection functionality
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
import json

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question
from admin_panel.views import DetectDuplicatesAPIView

User = get_user_model()


class DuplicateDetectionTestCase(TestCase):
    """Test cases for duplicate question detection"""
    
    def setUp(self):
        """Set up test data"""
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create test subject and class level
        self.subject = Subject.objects.create(
            name='Mathematics',
            description='Math subject for testing'
        )
        
        self.class_level = ClassLevel.objects.create(
            subject=self.subject,
            name='Grade 5',
            level_number=5
        )
        
        # Create test topic
        self.topic = Topic.objects.create(
            class_level=self.class_level,
            title='Addition and Subtraction',
            description='Basic arithmetic operations'
        )
        
        # Create test questions with duplicates
        self.question1 = Question.objects.create(
            topic=self.topic,
            question_text='What is 2 + 2?',
            question_type='multiple_choice',
            correct_answer='4',
            created_by=self.admin_user
        )
        
        # Exact duplicate
        self.question2 = Question.objects.create(
            topic=self.topic,
            question_text='What is 2 + 2?',
            question_type='multiple_choice',
            correct_answer='4',
            created_by=self.admin_user
        )
        
        # Near duplicate (with extra spaces and punctuation)
        self.question3 = Question.objects.create(
            topic=self.topic,
            question_text='What is 2+2 ?',
            question_type='multiple_choice',
            correct_answer='4',
            created_by=self.admin_user
        )
        
        # Different question
        self.question4 = Question.objects.create(
            topic=self.topic,
            question_text='What is 3 + 3?',
            question_type='multiple_choice',
            correct_answer='6',
            created_by=self.admin_user
        )
        
        self.client = Client()
        self.client.force_login(self.admin_user)
    
    def test_duplicate_detection_view_access(self):
        """Test that the duplicate detection page is accessible"""
        url = reverse('admin_panel:duplicate_questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Duplicate Questions Management')
    
    def test_similarity_calculation(self):
        """Test the similarity calculation method"""
        view = DetectDuplicatesAPIView()
        
        # Test exact match
        similarity = view.similarity('What is 2 + 2?', 'What is 2 + 2?')
        self.assertEqual(similarity, 1.0)
        
        # Test near match
        similarity = view.similarity('What is 2 + 2?', 'What is 2+2 ?')
        self.assertGreater(similarity, 0.8)
        
        # Test different questions
        similarity = view.similarity('What is 2 + 2?', 'What is 3 + 3?')
        self.assertLess(similarity, 0.8)
    
    def test_clean_question_text(self):
        """Test the question text cleaning method"""
        view = DetectDuplicatesAPIView()
        
        # Test HTML tag removal
        cleaned = view.clean_question_text('<p>What is 2 + 2?</p>')
        self.assertEqual(cleaned, 'what is 2 + 2?')
        
        # Test whitespace normalization
        cleaned = view.clean_question_text('What   is    2 + 2?')
        self.assertEqual(cleaned, 'what is 2 + 2?')
        
        # Test special character handling
        cleaned = view.clean_question_text('What is 2+2 ?')
        self.assertEqual(cleaned, 'what is 2+2 ?')
    
    def test_duplicate_detection_api(self):
        """Test the duplicate detection API endpoint"""
        url = reverse('admin_panel:api_detect_duplicates')
        
        data = {
            'similarity_threshold': 0.85
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertGreater(response_data['total_groups'], 0)
        self.assertGreater(response_data['total_duplicates'], 0)
    
    def test_duplicate_detection_with_filters(self):
        """Test duplicate detection with class level and subject filters"""
        url = reverse('admin_panel:api_detect_duplicates')
        
        data = {
            'class_level': 5,
            'subject': str(self.subject.id),
            'similarity_threshold': 0.85
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Should find duplicates in our test data
        if response_data['total_groups'] > 0:
            # Verify the duplicate group contains our test questions
            group = response_data['duplicates'][0]
            question_ids = [q['id'] for q in group['questions']]
            self.assertIn(str(self.question1.id), question_ids)
            self.assertIn(str(self.question2.id), question_ids)
    
    def test_delete_duplicates_safety(self):
        """Test that deletion preserves at least one copy"""
        url = reverse('admin_panel:api_delete_duplicates')
        
        # Try to delete all questions in a group
        data = {
            'action': 'group',
            'group_id': str(self.question1.id),
            'question_ids': [str(self.question1.id), str(self.question2.id)]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['preserved_count'], 1)
        
        # Verify that at least one question still exists
        remaining_questions = Question.objects.filter(
            id__in=[self.question1.id, self.question2.id]
        )
        self.assertEqual(remaining_questions.count(), 1)
    
    def test_unauthorized_access(self):
        """Test that non-admin users cannot access duplicate management"""
        # Create regular user
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='testpass123'
        )
        
        client = Client()
        client.force_login(regular_user)
        
        # Test page access
        url = reverse('admin_panel:duplicate_questions')
        response = client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test API access
        url = reverse('admin_panel:api_detect_duplicates')
        response = client.post(url, data='{}', content_type='application/json')
        self.assertEqual(response.status_code, 302)  # Redirect to login
