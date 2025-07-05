#!/usr/bin/env python
"""
Add Comprehensive Real-Life Grammar and Tenses Quizzes
Extensive quizzes covering all grammar concepts with practical applications
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def add_comprehensive_grammar_quizzes():
    """Add extensive real-life grammar and tenses quizzes"""
    print("ADDING COMPREHENSIVE GRAMMAR AND TENSES QUIZZES")
    print("=" * 60)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Grammar and Sentence Structure", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        print(f"Current questions: {topic.questions.count()}")
        
        # Comprehensive real-life grammar questions
        questions = [
            # Parts of Speech Questions
            {
                'question_text': 'You\'re writing a text to your friend: "My sister and I are going to the new movie theater." What part of speech is "new" in this sentence?',
                'choices': [
                    {'text': 'Noun', 'is_correct': False},
                    {'text': 'Verb', 'is_correct': False},
                    {'text': 'Adjective', 'is_correct': True},
                    {'text': 'Adverb', 'is_correct': False}
                ],
                'explanation': '"New" is an adjective because it describes the noun "movie theater." Adjectives tell us more about nouns.'
            },
            {
                'question_text': 'In a social media post, someone writes: "They quickly ran to catch the bus." What part of speech is "quickly"?',
                'choices': [
                    {'text': 'Adjective', 'is_correct': False},
                    {'text': 'Adverb', 'is_correct': True},
                    {'text': 'Verb', 'is_correct': False},
                    {'text': 'Noun', 'is_correct': False}
                ],
                'explanation': '"Quickly" is an adverb because it describes HOW they ran. Adverbs often end in -ly and describe verbs.'
            },
            
            # Verb Tenses Questions
            {
                'question_text': 'Your friend asks what you did yesterday. Which sentence uses the correct past tense?',
                'choices': [
                    {'text': 'I go to the mall with my family.', 'is_correct': False},
                    {'text': 'I went to the mall with my family.', 'is_correct': True},
                    {'text': 'I will go to the mall with my family.', 'is_correct': False},
                    {'text': 'I am going to the mall with my family.', 'is_correct': False}
                ],
                'explanation': '"Went" is the past tense of "go." Since the action happened yesterday (past), we use past tense.'
            },
            {
                'question_text': 'You\'re telling someone about your plans for tomorrow. Which sentence is correct?',
                'choices': [
                    {'text': 'Tomorrow I visited my grandmother.', 'is_correct': False},
                    {'text': 'Tomorrow I visit my grandmother.', 'is_correct': False},
                    {'text': 'Tomorrow I will visit my grandmother.', 'is_correct': True},
                    {'text': 'Tomorrow I am visiting my grandmother.', 'is_correct': False}
                ],
                'explanation': 'For future plans, we use "will + verb" or "going to + verb." "Will visit" correctly shows future tense.'
            },
            {
                'question_text': 'You\'re describing what you\'re doing right now in a video call. Which sentence is correct?',
                'choices': [
                    {'text': 'I eat dinner.', 'is_correct': False},
                    {'text': 'I am eating dinner.', 'is_correct': True},
                    {'text': 'I ate dinner.', 'is_correct': False},
                    {'text': 'I will eat dinner.', 'is_correct': False}
                ],
                'explanation': '"Am eating" is present continuous tense, used for actions happening right now. The -ing form shows ongoing action.'
            },
            
            # Subject-Verb Agreement Questions
            {
                'question_text': 'You\'re writing an email about your family. Which sentence has correct subject-verb agreement?',
                'choices': [
                    {'text': 'My family are going on vacation.', 'is_correct': False},
                    {'text': 'My family is going on vacation.', 'is_correct': True},
                    {'text': 'My family were going on vacation.', 'is_correct': False},
                    {'text': 'My family am going on vacation.', 'is_correct': False}
                ],
                'explanation': '"Family" is a collective noun treated as singular, so it takes "is." Even though a family has multiple people, we think of it as one unit.'
            },
            {
                'question_text': 'In a group chat, someone writes: "Everyone are excited about the party." What\'s wrong with this sentence?',
                'choices': [
                    {'text': 'Nothing is wrong', 'is_correct': False},
                    {'text': 'Should be "Everyone is excited" - everyone is singular', 'is_correct': True},
                    {'text': 'Should be "Everyone were excited"', 'is_correct': False},
                    {'text': 'Should be "Everyone am excited"', 'is_correct': False}
                ],
                'explanation': '"Everyone" is always singular, even though it refers to multiple people. Singular subjects take singular verbs: "Everyone is."'
            },
            
            # Pronoun Questions
            {
                'question_text': 'You and your friend are talking about a mutual friend. Which sentence is correct?',
                'choices': [
                    {'text': 'Me and Sarah went to the store.', 'is_correct': False},
                    {'text': 'Sarah and me went to the store.', 'is_correct': False},
                    {'text': 'Sarah and I went to the store.', 'is_correct': True},
                    {'text': 'Sarah and myself went to the store.', 'is_correct': False}
                ],
                'explanation': 'Use "I" as a subject. Test: "I went to the store" sounds right, but "Me went to the store" doesn\'t. Always put the other person first.'
            },
            {
                'question_text': 'Your teacher asks who completed the project. Which response is grammatically correct?',
                'choices': [
                    {'text': 'Me and my partner did.', 'is_correct': False},
                    {'text': 'My partner and me did.', 'is_correct': False},
                    {'text': 'My partner and I did.', 'is_correct': True},
                    {'text': 'Myself and my partner did.', 'is_correct': False}
                ],
                'explanation': 'Use "I" when you\'re the subject doing the action. "My partner and I" is correct because both are subjects of "did."'
            },
            
            # Homophones and Common Mistakes
            {
                'question_text': 'You\'re texting about weekend plans: "We\'re going to meet at _____ house." Which word fits correctly?',
                'choices': [
                    {'text': 'there', 'is_correct': False},
                    {'text': 'their', 'is_correct': True},
                    {'text': 'they\'re', 'is_correct': False},
                    {'text': 'thier', 'is_correct': False}
                ],
                'explanation': '"Their" shows ownership - it\'s their house. "There" is a place, "they\'re" means "they are," and "thier" is a misspelling.'
            },
            {
                'question_text': 'In an email to your teacher, you write: "I hope _____ proud of my improvement." Which word is correct?',
                'choices': [
                    {'text': 'your', 'is_correct': False},
                    {'text': 'you\'re', 'is_correct': True},
                    {'text': 'youre', 'is_correct': False},
                    {'text': 'yore', 'is_correct': False}
                ],
                'explanation': '"You\'re" means "you are." The sentence means "I hope you are proud." "Your" shows ownership, like "your book."'
            },
            
            # Sentence Structure Questions
            {
                'question_text': 'You\'re writing a story and want to combine these ideas: "The movie was scary" and "I enjoyed it." Which is the best way?',
                'choices': [
                    {'text': 'The movie was scary I enjoyed it.', 'is_correct': False},
                    {'text': 'The movie was scary, but I enjoyed it.', 'is_correct': True},
                    {'text': 'The movie was scary and I enjoyed it.', 'is_correct': False},
                    {'text': 'The movie was scary. And I enjoyed it.', 'is_correct': False}
                ],
                'explanation': 'Use "but" to show contrast between two ideas. The comma before "but" is needed when joining two complete sentences.'
            },
            {
                'question_text': 'Which of these is a complete sentence that you could use in a text message?',
                'choices': [
                    {'text': 'Running to catch the bus.', 'is_correct': False},
                    {'text': 'Because I was late.', 'is_correct': False},
                    {'text': 'I missed the bus.', 'is_correct': True},
                    {'text': 'When the alarm didn\'t go off.', 'is_correct': False}
                ],
                'explanation': '"I missed the bus" has a subject (I) and a predicate (missed the bus). The others are fragments - incomplete thoughts.'
            },
            
            # Capitalization and Punctuation
            {
                'question_text': 'You\'re writing about your vacation plans. Which sentence has correct capitalization?',
                'choices': [
                    {'text': 'we\'re going to disney world in florida next summer.', 'is_correct': False},
                    {'text': 'We\'re going to Disney World in Florida next Summer.', 'is_correct': False},
                    {'text': 'We\'re going to Disney World in Florida next summer.', 'is_correct': True},
                    {'text': 'We\'re Going To Disney World In Florida Next Summer.', 'is_correct': False}
                ],
                'explanation': 'Capitalize proper nouns (Disney World, Florida) and the first word of sentences. Seasons (summer) are not capitalized unless they start a sentence.'
            },
            {
                'question_text': 'You\'re writing a list for a group project. Which sentence is punctuated correctly?',
                'choices': [
                    {'text': 'We need markers, paper, glue and scissors.', 'is_correct': False},
                    {'text': 'We need markers paper glue and scissors.', 'is_correct': False},
                    {'text': 'We need markers, paper, glue, and scissors.', 'is_correct': True},
                    {'text': 'We need markers; paper; glue; and scissors.', 'is_correct': False}
                ],
                'explanation': 'Use commas to separate items in a list. The comma before "and" (Oxford comma) is recommended for clarity.'
            },
            
            # Advanced Grammar Applications
            {
                'question_text': 'You\'re giving a presentation and want to sound professional. Which sentence is most appropriate?',
                'choices': [
                    {'text': 'Me and my team worked really hard on this.', 'is_correct': False},
                    {'text': 'My team and I worked diligently on this project.', 'is_correct': True},
                    {'text': 'My team and me worked really hard on this.', 'is_correct': False},
                    {'text': 'Myself and my team worked really hard on this.', 'is_correct': False}
                ],
                'explanation': '"My team and I" is correct grammar, and "diligently" is more formal than "really hard," making it appropriate for presentations.'
            },
            {
                'question_text': 'In a formal email to your principal, which sentence demonstrates proper grammar and tone?',
                'choices': [
                    {'text': 'I would like to request a meeting to discuss my concerns.', 'is_correct': True},
                    {'text': 'I wanna talk to you about some stuff that\'s bugging me.', 'is_correct': False},
                    {'text': 'Can me and you meet up to chat about things?', 'is_correct': False},
                    {'text': 'I need to talk at you about problems.', 'is_correct': False}
                ],
                'explanation': 'Formal writing requires complete sentences, proper grammar, and respectful tone. "Would like to request" is polite and professional.'
            },
            
            # Real-World Application Questions
            {
                'question_text': 'You\'re helping a younger student with their writing. They wrote: "The dogs tail was wagging." What should you tell them?',
                'choices': [
                    {'text': 'It\'s perfect as written', 'is_correct': False},
                    {'text': 'Add an apostrophe: "The dog\'s tail was wagging"', 'is_correct': True},
                    {'text': 'Change it to: "The dogs tails was wagging"', 'is_correct': False},
                    {'text': 'Change "was" to "were"', 'is_correct': False}
                ],
                'explanation': 'Use an apostrophe to show possession. "The dog\'s tail" means the tail belongs to the dog. Without the apostrophe, it looks like multiple dogs.'
            },
            {
                'question_text': 'You\'re editing your friend\'s college application essay. They wrote: "I have went to volunteer at the animal shelter." How should this be corrected?',
                'choices': [
                    {'text': 'Leave it as is', 'is_correct': False},
                    {'text': 'Change to "I have gone to volunteer at the animal shelter"', 'is_correct': True},
                    {'text': 'Change to "I have going to volunteer at the animal shelter"', 'is_correct': False},
                    {'text': 'Change to "I went to volunteer at the animal shelter"', 'is_correct': False}
                ],
                'explanation': 'With "have," use the past participle "gone," not the simple past "went." "Have gone" is present perfect tense.'
            },
            {
                'question_text': 'You\'re writing a thank-you note after a job interview. Which sentence shows the best grammar and professionalism?',
                'choices': [
                    {'text': 'Thank you for taking the time to meet with me yesterday.', 'is_correct': True},
                    {'text': 'Thanks for meeting with me yesterday, it was great.', 'is_correct': False},
                    {'text': 'Thank you for yesterday when we met up.', 'is_correct': False},
                    {'text': 'Thanks for the meeting yesterday.', 'is_correct': False}
                ],
                'explanation': 'The first option is complete, formal, and specific. It shows professionalism and proper sentence structure for business communication.'
            }
        ]
        
        # Add questions to database
        questions_added = 0
        current_order = topic.questions.count()
        
        for i, q_data in enumerate(questions):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': 'multiple_choice',
                    'explanation': q_data['explanation'],
                    'order': current_order + i + 1,
                    'time_limit': 60,  # Grammar questions need thinking time
                    'is_active': True
                }
            )
            
            if created:
                print(f"  ✅ Added: {q_data['question_text'][:60]}...")
                questions_added += 1
                
                # Add answer choices
                for j, choice_data in enumerate(q_data['choices']):
                    AnswerChoice.objects.create(
                        question=question,
                        choice_text=choice_data['text'],
                        is_correct=choice_data['is_correct'],
                        order=j + 1
                    )
            else:
                print(f"  ⏭️  Skipped: {q_data['question_text'][:60]}... (already exists)")
        
        print(f"\n📊 SUMMARY:")
        print(f"New questions added: {questions_added}")
        print(f"Total questions now: {topic.questions.count()}")
        print("🎯 Grammar topic now has extensive real-life quizzes!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Add comprehensive grammar quizzes"""
    success = add_comprehensive_grammar_quizzes()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Grammar and Sentence Structure now has comprehensive real-life quizzes!")
        print("Students can practice grammar in practical, everyday contexts.")
    else:
        print("\n❌ FAILED!")
        print("Could not add quizzes. Check the error above.")

if __name__ == '__main__':
    main()
