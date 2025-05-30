from django.core.management.base import BaseCommand
from django.db.models import Count, Avg
from subjects.models import Topic, Subject, ClassLevel
from content.models import Question, Quiz
from content.utils import get_quiz_statistics, calculate_recommended_questions


class Command(BaseCommand):
    help = 'Display quiz statistics for all topics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--subject',
            type=str,
            help='Filter by subject name',
        )
        parser.add_argument(
            '--level',
            type=int,
            help='Filter by class level number',
        )
        parser.add_argument(
            '--topic',
            type=str,
            help='Filter by topic title',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📊 Quiz Statistics Report\n' + '='*50)
        )

        # Filter topics based on options
        topics = Topic.objects.filter(is_active=True)
        
        if options['subject']:
            topics = topics.filter(class_level__subject__name__icontains=options['subject'])
        
        if options['level']:
            topics = topics.filter(class_level__level_number=options['level'])
            
        if options['topic']:
            topics = topics.filter(title__icontains=options['topic'])

        if not topics.exists():
            self.stdout.write(
                self.style.WARNING('No topics found matching the criteria.')
            )
            return

        total_topics = topics.count()
        topics_with_questions = 0
        total_questions = 0
        total_quizzes_taken = 0

        self.stdout.write(f"\n📚 Found {total_topics} topics:\n")

        for topic in topics.select_related('class_level__subject'):
            stats = get_quiz_statistics(topic)
            recommended = calculate_recommended_questions(stats['total_questions'])
            
            # Count quizzes taken for this topic
            quiz_count = Quiz.objects.filter(topic=topic).count()
            avg_score = Quiz.objects.filter(topic=topic, is_completed=True).aggregate(
                avg_score=Avg('percentage')
            )['avg_score'] or 0

            if stats['total_questions'] > 0:
                topics_with_questions += 1
                total_questions += stats['total_questions']
                total_quizzes_taken += quiz_count

                # Topic header
                self.stdout.write(
                    f"\n🎯 {topic.class_level.subject.name} - {topic.class_level.name} - {topic.title}"
                )
                self.stdout.write("-" * 60)
                
                # Question statistics
                self.stdout.write(f"📝 Questions Available: {stats['total_questions']}")
                self.stdout.write(f"   • Easy: {stats['easy_questions']}")
                self.stdout.write(f"   • Medium: {stats['medium_questions']}")
                self.stdout.write(f"   • Hard: {stats['hard_questions']}")
                
                # Question types
                self.stdout.write(f"📋 Question Types:")
                self.stdout.write(f"   • Multiple Choice: {stats['multiple_choice']}")
                self.stdout.write(f"   • Fill in Blank: {stats['fill_blank']}")
                self.stdout.write(f"   • True/False: {stats['true_false']}")
                
                # Quiz configuration
                self.stdout.write(f"⚙️  Quiz Configuration:")
                self.stdout.write(f"   • Recommended Questions: {recommended}")
                self.stdout.write(f"   • Questions Used: {min(recommended, stats['total_questions'])}")
                
                # Usage statistics
                self.stdout.write(f"📊 Usage Statistics:")
                self.stdout.write(f"   • Quizzes Taken: {quiz_count}")
                self.stdout.write(f"   • Average Score: {avg_score:.1f}%")
                
                # Shuffling info
                if stats['total_questions'] > recommended:
                    self.stdout.write(f"🔀 Shuffling: Enabled (selecting {recommended} from {stats['total_questions']})")
                else:
                    self.stdout.write(f"🔀 Shuffling: All questions used")
                    
            else:
                self.stdout.write(
                    f"\n⚠️  {topic.class_level.subject.name} - {topic.class_level.name} - {topic.title}"
                )
                self.stdout.write("   No questions available")

        # Summary
        self.stdout.write(f"\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("📈 SUMMARY"))
        self.stdout.write(f"Total Topics: {total_topics}")
        self.stdout.write(f"Topics with Questions: {topics_with_questions}")
        self.stdout.write(f"Topics without Questions: {total_topics - topics_with_questions}")
        self.stdout.write(f"Total Questions: {total_questions}")
        self.stdout.write(f"Total Quizzes Taken: {total_quizzes_taken}")
        
        if topics_with_questions > 0:
            avg_questions_per_topic = total_questions / topics_with_questions
            self.stdout.write(f"Average Questions per Topic: {avg_questions_per_topic:.1f}")
            
        # Recommendations
        self.stdout.write(f"\n💡 RECOMMENDATIONS:")
        if total_topics - topics_with_questions > 0:
            self.stdout.write(f"• Add questions to {total_topics - topics_with_questions} topics without content")
        
        low_question_topics = [
            topic for topic in topics 
            if get_quiz_statistics(topic)['total_questions'] < 5
            and get_quiz_statistics(topic)['total_questions'] > 0
        ]
        
        if low_question_topics:
            self.stdout.write(f"• Consider adding more questions to {len(low_question_topics)} topics with < 5 questions")
            
        self.stdout.write(f"• Current shuffling system ensures fair assessment across attempts")
