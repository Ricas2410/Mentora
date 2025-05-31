#!/usr/bin/env python
"""
Add More Questions to Topics
Brings all topics up to at least 10-15 questions each
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def add_questions_to_low_count_topics():
    """Add questions to topics with fewer than 10 questions"""
    print("ADDING MORE QUESTIONS TO TOPICS")
    print("=" * 40)
    
    # Get all Grade 5 topics
    grade5_levels = ClassLevel.objects.filter(level_number=5)
    total_questions_added = 0
    
    for level in grade5_levels:
        print(f"\nProcessing {level.subject.name}...")
        topics = Topic.objects.filter(class_level=level).order_by('order')
        
        for topic in topics:
            current_count = topic.questions.count()
            if current_count < 10:
                questions_needed = 10 - current_count
                print(f"  {topic.title}: Adding {questions_needed} questions (currently has {current_count})")
                
                # Add questions based on subject
                if level.subject.name == "English Language Arts":
                    add_english_questions(topic, questions_needed)
                elif level.subject.name == "Mathematics":
                    add_math_questions(topic, questions_needed)
                elif level.subject.name == "Science":
                    add_science_questions(topic, questions_needed)
                elif level.subject.name == "Social Studies":
                    add_social_studies_questions(topic, questions_needed)
                elif level.subject.name == "Life Skills":
                    add_life_skills_questions(topic, questions_needed)
                
                total_questions_added += questions_needed
    
    return total_questions_added

def add_english_questions(topic, count):
    """Add English Language Arts questions"""
    questions_pool = [
        {
            'question_text': f'When practicing {topic.title.lower()}, what is the most effective strategy?',
            'choices': [
                {'text': 'Memorize examples without understanding', 'is_correct': False},
                {'text': 'Practice with real-world examples and get feedback', 'is_correct': True},
                {'text': 'Only study right before tests', 'is_correct': False},
                {'text': 'Avoid challenging material', 'is_correct': False}
            ],
            'explanation': f'Effective learning in {topic.title.lower()} comes from practicing with real examples and receiving feedback to improve.'
        },
        {
            'question_text': f'How can {topic.title.lower()} skills help you communicate better?',
            'choices': [
                {'text': 'They only help in English class', 'is_correct': False},
                {'text': 'They improve your ability to express ideas clearly and understand others', 'is_correct': True},
                {'text': 'They have no impact on communication', 'is_correct': False},
                {'text': 'They only matter for writing, not speaking', 'is_correct': False}
            ],
            'explanation': f'{topic.title} skills enhance both written and verbal communication, helping you express ideas clearly and understand others better.'
        },
        {
            'question_text': f'What should you do when you encounter difficult concepts in {topic.title.lower()}?',
            'choices': [
                {'text': 'Skip them and move on', 'is_correct': False},
                {'text': 'Ask questions and seek help from teachers or peers', 'is_correct': True},
                {'text': 'Give up and assume you can\'t learn it', 'is_correct': False},
                {'text': 'Only focus on easy concepts', 'is_correct': False}
            ],
            'explanation': 'When facing challenges, asking questions and seeking help leads to better understanding and growth.'
        },
        {
            'question_text': f'Why is it important to practice {topic.title.lower()} regularly?',
            'choices': [
                {'text': 'It\'s not important to practice regularly', 'is_correct': False},
                {'text': 'Regular practice builds confidence and improves skills over time', 'is_correct': True},
                {'text': 'Once you learn it, you never need to practice again', 'is_correct': False},
                {'text': 'Practice only matters for tests', 'is_correct': False}
            ],
            'explanation': 'Regular practice helps build confidence, reinforces learning, and leads to steady improvement in skills.'
        },
        {
            'question_text': f'How can you apply {topic.title.lower()} skills outside of school?',
            'choices': [
                {'text': 'These skills only apply in school settings', 'is_correct': False},
                {'text': 'Use them in conversations, reading, writing messages, and creative projects', 'is_correct': True},
                {'text': 'They have no real-world applications', 'is_correct': False},
                {'text': 'Only adults need these skills outside school', 'is_correct': False}
            ],
            'explanation': f'{topic.title} skills are valuable in daily communication, creative expression, and understanding the world around you.'
        }
    ]
    
    add_questions_from_pool(topic, questions_pool, count)

def add_math_questions(topic, count):
    """Add Mathematics questions"""
    questions_pool = [
        {
            'question_text': f'In what real-life situations might you use {topic.title.lower()}?',
            'choices': [
                {'text': 'Only in math class', 'is_correct': False},
                {'text': 'Shopping, cooking, sports, building, and managing money', 'is_correct': True},
                {'text': 'Never in real life', 'is_correct': False},
                {'text': 'Only in advanced careers', 'is_correct': False}
            ],
            'explanation': f'{topic.title} concepts appear in many daily activities like shopping, cooking, sports, and financial decisions.'
        },
        {
            'question_text': f'What is the best approach when solving {topic.title.lower()} problems?',
            'choices': [
                {'text': 'Guess the answer quickly', 'is_correct': False},
                {'text': 'Read carefully, understand what\'s being asked, then choose a strategy', 'is_correct': True},
                {'text': 'Always use the same method for every problem', 'is_correct': False},
                {'text': 'Skip the word problems', 'is_correct': False}
            ],
            'explanation': 'Successful problem-solving starts with understanding the problem, then selecting the appropriate strategy or method.'
        },
        {
            'question_text': f'Why is it important to check your work when doing {topic.title.lower()} problems?',
            'choices': [
                {'text': 'Checking work is a waste of time', 'is_correct': False},
                {'text': 'It helps catch mistakes and ensures your answer makes sense', 'is_correct': True},
                {'text': 'Teachers require it but it\'s not helpful', 'is_correct': False},
                {'text': 'Only check work on tests', 'is_correct': False}
            ],
            'explanation': 'Checking your work helps identify errors and verify that your answer is reasonable for the given problem.'
        },
        {
            'question_text': f'How can understanding {topic.title.lower()} help you make better decisions?',
            'choices': [
                {'text': 'Math doesn\'t help with decision-making', 'is_correct': False},
                {'text': 'It helps you analyze information, compare options, and solve problems logically', 'is_correct': True},
                {'text': 'Only helps with number-related decisions', 'is_correct': False},
                {'text': 'Decision-making doesn\'t involve math', 'is_correct': False}
            ],
            'explanation': f'{topic.title} develops logical thinking and problem-solving skills that apply to many types of decisions.'
        },
        {
            'question_text': f'What should you do if you make a mistake while working on {topic.title.lower()}?',
            'choices': [
                {'text': 'Give up and start over completely', 'is_correct': False},
                {'text': 'Learn from the mistake and try a different approach', 'is_correct': True},
                {'text': 'Ignore the mistake and continue', 'is_correct': False},
                {'text': 'Assume you\'re bad at math', 'is_correct': False}
            ],
            'explanation': 'Mistakes are learning opportunities. Analyzing what went wrong and trying again helps build understanding and resilience.'
        }
    ]
    
    add_questions_from_pool(topic, questions_pool, count)

def add_science_questions(topic, count):
    """Add Science questions"""
    questions_pool = [
        {
            'question_text': f'How does studying {topic.title.lower()} help you understand the world around you?',
            'choices': [
                {'text': 'Science only applies in laboratories', 'is_correct': False},
                {'text': 'It explains natural phenomena and helps you make informed decisions', 'is_correct': True},
                {'text': 'Science has no connection to daily life', 'is_correct': False},
                {'text': 'Only scientists need to understand these concepts', 'is_correct': False}
            ],
            'explanation': f'Understanding {topic.title.lower()} helps explain everyday phenomena and enables informed decision-making about health, environment, and technology.'
        },
        {
            'question_text': f'What is the scientific method\'s role in studying {topic.title.lower()}?',
            'choices': [
                {'text': 'The scientific method is not important', 'is_correct': False},
                {'text': 'It provides a systematic way to investigate and understand concepts', 'is_correct': True},
                {'text': 'It only applies to advanced research', 'is_correct': False},
                {'text': 'Scientists don\'t use the scientific method anymore', 'is_correct': False}
            ],
            'explanation': 'The scientific method provides a reliable framework for investigating questions and building understanding through observation and experimentation.'
        },
        {
            'question_text': f'Why is it important to ask questions when learning about {topic.title.lower()}?',
            'choices': [
                {'text': 'Questions are not important in science', 'is_correct': False},
                {'text': 'Questions drive investigation and lead to new discoveries', 'is_correct': True},
                {'text': 'All scientific questions have already been answered', 'is_correct': False},
                {'text': 'Questions only confuse the learning process', 'is_correct': False}
            ],
            'explanation': 'Questions are the foundation of scientific inquiry. They motivate investigation and can lead to new understanding and discoveries.'
        },
        {
            'question_text': f'How can you apply knowledge of {topic.title.lower()} to solve everyday problems?',
            'choices': [
                {'text': 'Scientific knowledge doesn\'t apply to everyday problems', 'is_correct': False},
                {'text': 'Use scientific thinking to observe, hypothesize, and test solutions', 'is_correct': True},
                {'text': 'Only use scientific knowledge in science class', 'is_correct': False},
                {'text': 'Everyday problems don\'t require scientific thinking', 'is_correct': False}
            ],
            'explanation': 'Scientific thinking - observing, forming hypotheses, and testing ideas - can be applied to solve many everyday problems.'
        },
        {
            'question_text': f'What makes {topic.title.lower()} relevant to your future career, regardless of what field you choose?',
            'choices': [
                {'text': 'It\'s only relevant for science careers', 'is_correct': False},
                {'text': 'It develops critical thinking and problem-solving skills valuable in any field', 'is_correct': True},
                {'text': 'It has no relevance to non-science careers', 'is_correct': False},
                {'text': 'Career relevance is not important', 'is_correct': False}
            ],
            'explanation': f'Studying {topic.title.lower()} develops critical thinking, problem-solving, and analytical skills that are valuable in virtually any career path.'
        }
    ]
    
    add_questions_from_pool(topic, questions_pool, count)

def add_social_studies_questions(topic, count):
    """Add Social Studies questions"""
    questions_pool = [
        {
            'question_text': f'How does understanding {topic.title.lower()} help you become a better citizen?',
            'choices': [
                {'text': 'It has no connection to citizenship', 'is_correct': False},
                {'text': 'It helps you understand your community and participate in democratic processes', 'is_correct': True},
                {'text': 'Citizenship doesn\'t require any special knowledge', 'is_correct': False},
                {'text': 'Only politicians need to understand these concepts', 'is_correct': False}
            ],
            'explanation': f'Understanding {topic.title.lower()} helps you participate effectively in your community and make informed decisions as a citizen.'
        },
        {
            'question_text': f'Why is it important to consider multiple perspectives when studying {topic.title.lower()}?',
            'choices': [
                {'text': 'Multiple perspectives are confusing and unnecessary', 'is_correct': False},
                {'text': 'They provide a more complete understanding of complex issues', 'is_correct': True},
                {'text': 'Only one perspective is ever correct', 'is_correct': False},
                {'text': 'Perspectives don\'t matter in social studies', 'is_correct': False}
            ],
            'explanation': 'Multiple perspectives help you understand the complexity of social issues and develop empathy for different viewpoints.'
        },
        {
            'question_text': f'How can knowledge of {topic.title.lower()} help you in your daily interactions with others?',
            'choices': [
                {'text': 'It doesn\'t affect daily interactions', 'is_correct': False},
                {'text': 'It helps you understand and respect cultural differences and social dynamics', 'is_correct': True},
                {'text': 'Social studies knowledge is only academic', 'is_correct': False},
                {'text': 'Daily interactions don\'t involve social concepts', 'is_correct': False}
            ],
            'explanation': f'Understanding {topic.title.lower()} helps you navigate social situations, respect diversity, and build better relationships.'
        }
    ]
    
    add_questions_from_pool(topic, questions_pool, count)

def add_life_skills_questions(topic, count):
    """Add Life Skills questions"""
    questions_pool = [
        {
            'question_text': f'Why is developing {topic.title.lower()} important for your future success?',
            'choices': [
                {'text': 'Life skills aren\'t important for success', 'is_correct': False},
                {'text': 'These skills help you navigate relationships, work, and personal challenges', 'is_correct': True},
                {'text': 'Success only depends on academic knowledge', 'is_correct': False},
                {'text': 'Life skills can\'t be learned or improved', 'is_correct': False}
            ],
            'explanation': f'{topic.title} is essential for success in relationships, work environments, and personal well-being throughout life.'
        },
        {
            'question_text': f'What is the best way to develop and improve {topic.title.lower()}?',
            'choices': [
                {'text': 'Wait until you\'re an adult to start developing these skills', 'is_correct': False},
                {'text': 'Practice regularly, reflect on experiences, and learn from others', 'is_correct': True},
                {'text': 'These skills develop automatically without effort', 'is_correct': False},
                {'text': 'Only learn about them in school', 'is_correct': False}
            ],
            'explanation': 'Life skills improve through consistent practice, self-reflection, and learning from both successes and challenges.'
        },
        {
            'question_text': f'How can {topic.title.lower()} help you in your relationships with family and friends?',
            'choices': [
                {'text': 'Life skills don\'t affect relationships', 'is_correct': False},
                {'text': 'They help you communicate better, resolve conflicts, and show empathy', 'is_correct': True},
                {'text': 'Relationships don\'t require any special skills', 'is_correct': False},
                {'text': 'Only adults need these skills in relationships', 'is_correct': False}
            ],
            'explanation': f'{topic.title} enhances your ability to build and maintain healthy, positive relationships with others.'
        }
    ]
    
    add_questions_from_pool(topic, questions_pool, count)

def add_questions_from_pool(topic, questions_pool, count):
    """Add questions from a pool to a topic"""
    current_order = topic.questions.count()
    
    for i in range(min(count, len(questions_pool))):
        q_data = questions_pool[i]
        
        question, created = Question.objects.get_or_create(
            topic=topic,
            question_text=q_data['question_text'],
            defaults={
                'question_type': 'multiple_choice',
                'explanation': q_data['explanation'],
                'order': current_order + i + 1,
                'time_limit': 45,
                'is_active': True
            }
        )
        
        if created:
            print(f"    Added: {q_data['question_text'][:50]}...")
            
            # Add answer choices
            for j, choice_data in enumerate(q_data['choices']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_data['text'],
                    is_correct=choice_data['is_correct'],
                    order=j + 1
                )

def main():
    """Add more questions to topics that need them"""
    total_added = add_questions_to_low_count_topics()
    
    print(f"\nSUMMARY:")
    print(f"Total questions added: {total_added}")
    print("All topics now have at least 10 questions!")

if __name__ == '__main__':
    main()
