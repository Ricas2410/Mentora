#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from content.models import Question

def update_questions():
    """Update questions to have multiple acceptable answers"""
    
    try:
        # Update the rhyming question to accept multiple rhymes
        q1 = Question.objects.get(id='144e0ec7-8c63-419a-8efb-5b7a1dd5fa8a')
        q1.correct_answer = 'top, pop, stop, shop, drop, cop, mop'
        q1.explanation = 'Words that rhyme with "hop" include: top, pop, stop, shop, drop, cop, mop, and many others.'
        q1.save()
        print(f'Updated rhyming question: {q1.correct_answer}')

        # Update the sentence completion to accept multiple answers
        q2 = Question.objects.get(id='d910454b-e934-4a86-82fb-cbbde4469683')
        q2.correct_answer = 'flies, sings, chirps, soars, tweets'
        q2.explanation = 'Birds can fly, sing, chirp, soar, tweet, and perform many other actions.'
        q2.save()
        print(f'Updated sentence completion: {q2.correct_answer}')

        # Update the first letter question to accept both cases
        q3 = Question.objects.get(id='51bb628a-9ccd-41d5-9aa1-b5a44aa25b80')
        q3.correct_answer = 'A, a'
        q3.explanation = 'The first letter of the alphabet is A (uppercase) or a (lowercase).'
        q3.save()
        print(f'Updated alphabet question: {q3.correct_answer}')

        # Create a new synonym question to demonstrate the intelligent matching
        from subjects.models import Topic
        topic = Topic.objects.filter(questions__isnull=False).first()
        
        # Check if synonym question already exists
        synonym_question = Question.objects.filter(question_text__icontains='synonym for "intelligent"').first()
        if not synonym_question:
            synonym_question = Question.objects.create(
                topic=topic,
                question_text='Give a synonym for "intelligent".',
                question_type='short_answer',
                correct_answer='smart, clever, bright, wise, brilliant, sharp',
                explanation='Smart, clever, bright, wise, brilliant, and sharp are all synonyms for intelligent.',
                difficulty='easy',
                points=1,
                time_limit=45,
                explanation_display_time=5
            )
            print(f'Created new synonym question: {synonym_question.correct_answer}')
        else:
            synonym_question.correct_answer = 'smart, clever, bright, wise, brilliant, sharp'
            synonym_question.explanation = 'Smart, clever, bright, wise, brilliant, and sharp are all synonyms for intelligent.'
            synonym_question.save()
            print(f'Updated existing synonym question: {synonym_question.correct_answer}')

        print('Successfully updated questions with multiple acceptable answers!')
        
    except Exception as e:
        print(f'Error updating questions: {e}')

if __name__ == '__main__':
    update_questions()
