from django import forms
from django.core.validators import FileExtensionValidator
from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote
from users.models import User
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    """Form for managing site settings"""

    class Meta:
        model = SiteSettings
        exclude = ['id', 'created_at', 'updated_at', 'updated_by']
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'site_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'site_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'site_favicon': forms.FileInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'minimum_pass_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'quiz_questions_per_topic': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 50}),
            'quiz_time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 60, 'max': 3600}),
            'question_time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 300}),
            'show_correct_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shuffle_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shuffle_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'allow_question_skip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_progress_bar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'exam_questions_per_subject': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 100}),
            'exam_time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 600, 'max': 14400}),
            'require_all_subjects_completion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'allow_retakes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_retake_attempts': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'enable_email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_verification_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'allow_file_uploads': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_file_size_mb': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'allowed_file_types': forms.TextInput(attrs={'class': 'form-control'}),
            'default_user_avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'default_subject_icon': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'default_hero_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'enable_user_registration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'require_strong_passwords': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'session_timeout_minutes': forms.Select(
                choices=[
                    (30, '30 minutes (Short sessions)'),
                    (60, '1 hour (Recommended)'),
                    (120, '2 hours (Extended)'),
                    (240, '4 hours (Long sessions)'),
                    (480, '8 hours (All day)'),
                ],
                attrs={'class': 'form-control'}
            ),
            'max_login_attempts': forms.NumberInput(attrs={'class': 'form-control', 'min': 3, 'max': 20}),
            'enable_offline_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_progress_tracking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_achievements': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_leaderboards': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_push_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_sms_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'daily_reminder_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'enable_content_moderation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'auto_approve_uploads': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'maintenance_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'maintenance_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 300}),
            'explanation_display_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'test_questions_per_topic': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'test_time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 300, 'max': 7200}),
            'exam_questions_per_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 200}),
            'exam_time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 600, 'max': 14400}),
            'max_retake_attempts': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'max_file_size_mb': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'allowed_file_types': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'pdf,doc,docx,txt,jpg,jpeg,png,gif'}),
            'maintenance_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SubjectForm(forms.ModelForm):
    """Enhanced form for creating/editing subjects with class level management"""

    # Grade level choices for multi-select
    GRADE_LEVEL_CHOICES = [
        (1, 'Grade 1 (Elementary)'),
        (2, 'Grade 2 (Elementary)'),
        (3, 'Grade 3 (Elementary)'),
        (4, 'Grade 4 (Elementary)'),
        (5, 'Grade 5 (Elementary)'),
        (6, 'Grade 6 (Elementary)'),
        (7, 'Grade 7 (Middle School)'),
        (8, 'Grade 8 (Middle School)'),
        (9, 'Grade 9 (Middle School)'),
        (10, 'Grade 10 (High School)'),
        (11, 'Grade 11 (High School)'),
        (12, 'Grade 12 (High School)'),
    ]

    class_levels = forms.MultipleChoiceField(
        choices=GRADE_LEVEL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        help_text="Select which grade levels should have this subject"
    )

    class Meta:
        model = Subject
        fields = ['name', 'description', 'icon', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Subject description'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FontAwesome icon class (e.g., fas fa-book)'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing existing subject, pre-select current class levels
        if self.instance and self.instance.pk:
            current_levels = list(self.instance.classlevels.values_list('level_number', flat=True))
            self.fields['class_levels'].initial = current_levels

    def save(self, commit=True):
        subject = super().save(commit=commit)

        if commit:
            # Get selected class levels
            selected_levels = [int(level) for level in self.cleaned_data['class_levels']]

            # Create or update ClassLevel objects for this subject
            for level_number in selected_levels:
                class_level, created = ClassLevel.objects.get_or_create(
                    subject=subject,
                    level_number=level_number,
                    defaults={
                        'name': f'Grade {level_number}',
                        'description': f'{subject.name} curriculum for Grade {level_number}',
                        'is_active': True
                    }
                )
                if not created:
                    # Update existing class level to be active
                    class_level.is_active = True
                    class_level.save()

            # Deactivate class levels not selected
            subject.classlevels.exclude(level_number__in=selected_levels).update(is_active=False)

        return subject


class ClassLevelForm(forms.ModelForm):
    """Form for creating/editing class levels"""

    # International Grade Level choices
    INTERNATIONAL_GRADE_CHOICES = [
        # Elementary School (Grades 1-6)
        ('Grade 1', 'Grade 1 (Elementary)'),
        ('Grade 2', 'Grade 2 (Elementary)'),
        ('Grade 3', 'Grade 3 (Elementary)'),
        ('Grade 4', 'Grade 4 (Elementary)'),
        ('Grade 5', 'Grade 5 (Elementary)'),
        ('Grade 6', 'Grade 6 (Elementary)'),
        # Middle School (Grades 7-9)
        ('Grade 7', 'Grade 7 (Middle School)'),
        ('Grade 8', 'Grade 8 (Middle School)'),
        ('Grade 9', 'Grade 9 (Middle School)'),
        # High School (Grades 10-12)
        ('Grade 10', 'Grade 10 (High School)'),
        ('Grade 11', 'Grade 11 (High School)'),
        ('Grade 12', 'Grade 12 (High School)'),
    ]

    name = forms.ChoiceField(
        choices=INTERNATIONAL_GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select from international grade levels (K-12 system)"
    )

    class Meta:
        model = ClassLevel
        fields = ['subject', 'name', 'level_number', 'description', 'is_active']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'level_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Level description'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level_number'].help_text = "This will be auto-populated based on your level selection"


class TopicForm(forms.ModelForm):
    """Form for creating/editing topics"""

    class Meta:
        model = Topic
        fields = ['class_level', 'title', 'description', 'difficulty_level', 'order', 'is_active']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topic title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Topic description'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""

    class Meta:
        model = Question
        fields = [
            'topic', 'question_text', 'question_type', 'difficulty',
            'explanation', 'time_limit', 'explanation_display_time', 'is_active'
        ]
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your question here'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Explanation for the correct answer'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 300}),
            'explanation_display_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AnswerChoiceForm(forms.ModelForm):
    """Form for creating/editing answer choices"""

    class Meta:
        model = AnswerChoice
        fields = ['choice_text', 'is_correct', 'order']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Answer choice text'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class StudyNoteForm(forms.ModelForm):
    """Form for creating/editing study notes"""

    class Meta:
        model = StudyNote
        fields = ['topic', 'title', 'content', 'image', 'audio_file', 'video_url', 'order', 'is_active']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note title'}),
            'content': forms.Textarea(attrs={'class': 'form-control summernote', 'rows': 10, 'placeholder': 'Note content (supports rich text)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'YouTube or video URL'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TopicForm(forms.ModelForm):
    """Form for creating/editing topics"""

    class Meta:
        model = Topic
        fields = ['class_level', 'title', 'description', 'estimated_duration', 'difficulty_level', 'order', 'is_active']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topic title'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote-compact', 'rows': 4, 'placeholder': 'Topic description'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 300}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""

    class Meta:
        model = Question
        fields = ['topic', 'question_text', 'question_type', 'difficulty', 'points', 'explanation', 'image', 'is_active']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control summernote-compact', 'rows': 4, 'placeholder': 'Enter your question here...'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'explanation': forms.Textarea(attrs={'class': 'form-control summernote-compact', 'rows': 3, 'placeholder': 'Explain the correct answer...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CSVImportForm(forms.Form):
    """Enhanced form for CSV import with class level selection"""

    # Grade level choices for multi-select
    GRADE_LEVEL_CHOICES = [
        (1, 'Grade 1 (Elementary)'),
        (2, 'Grade 2 (Elementary)'),
        (3, 'Grade 3 (Elementary)'),
        (4, 'Grade 4 (Elementary)'),
        (5, 'Grade 5 (Elementary)'),
        (6, 'Grade 6 (Elementary)'),
        (7, 'Grade 7 (Middle School)'),
        (8, 'Grade 8 (Middle School)'),
        (9, 'Grade 9 (Middle School)'),
        (10, 'Grade 10 (High School)'),
        (11, 'Grade 11 (High School)'),
        (12, 'Grade 12 (High School)'),
    ]

    csv_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        }),
        help_text="Upload a CSV file with questions (max 5MB). Download the template first."
    )

    target_class_levels = forms.MultipleChoiceField(
        choices=GRADE_LEVEL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        help_text="Select which grade levels these questions should be imported for. Missing topics will be auto-created."
    )

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("File size cannot exceed 5MB")
        return file


class UserEditForm(forms.ModelForm):
    """Form for editing user details by admin"""

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'current_class_level', 'learning_goals',
            'is_active', 'is_staff', 'is_email_verified'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'current_class_level': forms.Select(attrs={'class': 'form-control'}),
            'learning_goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_email_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Formset for managing multiple answer choices
AnswerChoiceFormSet = forms.inlineformset_factory(
    Question,
    AnswerChoice,
    form=AnswerChoiceForm,
    extra=4,
    max_num=6,
    can_delete=True,
    widgets={
        'choice_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Answer choice'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    }
)
