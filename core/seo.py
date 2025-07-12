"""
SEO optimization utilities for Pentora platform
Includes structured data, meta tags, and search engine optimization features
"""

from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json


class SEOManager:
    """
    Centralized SEO management for the platform
    """
    
    def __init__(self, request=None):
        self.request = request
        self.site_name = getattr(settings, 'SITE_NAME', 'Pentora - Ghana\'s #1 Online Education Platform')
        self.site_url = getattr(settings, 'SITE_URL', 'https://pentora.deigratiams.edu.gh')
    
    def get_meta_tags(self, title=None, description=None, keywords=None, image=None, url=None):
        """
        Generate comprehensive meta tags for SEO
        """
        # Default values - Enhanced for unique Pentora branding and Ghana dominance
        default_title = f"Pentora Ghana | {self.site_name} | Official Educational Platform"
        default_description = "Pentora Ghana - The official #1 online education platform in Ghana. Trusted by thousands of students for BECE preparation, WASSCE preparation, free quality education, and comprehensive learning materials. Join Ghana's leading educational community."
        default_keywords = "Pentora Ghana, Pentora education, Pentora official, Pentora learning platform, Pentora online school, Mentora learn, Mentora education, Ghana's best education platform, #1 education Ghana, top education platform Ghana, official Pentora, Pentora.edu.gh, online learning Ghana, free education Ghana, BECE preparation Ghana, WASSCE preparation Ghana, Ghana education platform, online studies Ghana, e-learning Ghana, digital education Ghana, educational platform Ghana, online school Ghana, free online learning Ghana, educational resources Ghana, study materials Ghana, online tutoring Ghana, distance learning Ghana, virtual classroom Ghana, EdTech Ghana, Ghana online education, learn online Ghana, education technology Ghana, online courses Ghana, free education platform Ghana, quality education Ghana, academic support Ghana, student learning Ghana, educational excellence Ghana, Ghana's premier education, leading education platform Ghana, trusted education Ghana, verified education platform Ghana, accredited online learning Ghana, certified education Ghana, authentic Pentora, genuine Pentora, real Pentora, original Pentora"
        default_image = f"{self.site_url}/static/images/Pentora-og-image.jpg"
        
        # Enhanced education keywords for better search visibility
        education_keywords = [
            'education', 'online learning', 'e-learning', 'digital education',
            'Mentora', 'Pentora', 'educational platform', 'online studies',
            'BECE preparation', 'WASSCE preparation', 'Ghana education',
            'primary education', 'secondary education', 'JHS', 'SHS',
            'mathematics', 'english', 'science', 'social studies',
            'online quizzes', 'study notes', 'exam preparation',
            'free education', 'quality education', 'academic excellence',
            'student learning', 'educational resources', 'study materials',
            'interactive learning', 'personalized education', 'learning platform',
            'educational technology', 'EdTech Ghana', 'online tutoring',
            'curriculum-based learning', 'grade-specific content',
            'comprehensive education', 'academic support', 'learning management',
            'distance learning', 'virtual classroom', 'educational app',
            'study platform', 'learning app', 'education Ghana', 'school online'
        ]

        # Use provided values or defaults
        title = title or default_title
        description = description or default_description
        base_keywords = keywords or default_keywords
        image = image or default_image
        url = url or (self.request.build_absolute_uri() if self.request else self.site_url)

        # Combine provided keywords with education keywords
        all_keywords = base_keywords.split(', ') if base_keywords else []
        all_keywords.extend(education_keywords)
        enhanced_keywords = ', '.join(list(dict.fromkeys(all_keywords)))  # Remove duplicates
        
        meta_tags = {
            'title': title,
            'description': description,
            'keywords': enhanced_keywords,
            'canonical_url': url,
            'author': 'Pentora Educational Platform - Quality Education for All',
            'robots': 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1',
            'viewport': 'width=device-width, initial-scale=1.0',
            'theme-color': '#3B82F6',
            'application-name': 'Pentora',
            'apple-mobile-web-app-title': 'Pentora Education',
            'apple-mobile-web-app-capable': 'yes',
            'mobile-web-app-capable': 'yes',
            'og_title': title,
            'og_description': description,
            'og_image': image,
            'og_url': url,
            'og_type': 'website',
            'og_site_name': 'Pentora Educational Platform',
            'twitter_card': 'summary_large_image',
            'twitter_title': title,
            'twitter_description': description,
            'twitter_image': image,
            'twitter_site': '@Pentora',
            'twitter_creator': '@Pentora',
        }
        
        return meta_tags
    
    def generate_structured_data(self, data_type, data):
        """
        Generate JSON-LD structured data for search engines
        """
        if data_type == 'organization':
            return self._generate_organization_schema(data)
        elif data_type == 'course':
            return self._generate_course_schema(data)
        elif data_type == 'quiz':
            return self._generate_quiz_schema(data)
        elif data_type == 'article':
            return self._generate_article_schema(data)
        elif data_type == 'breadcrumb':
            return self._generate_breadcrumb_schema(data)
        
        return None
    
    def _generate_organization_schema(self, data):
        """Generate Organization schema for Pentora as Ghana's #1 education platform"""
        schema = {
            "@context": "https://schema.org",
            "@type": "EducationalOrganization",
            "name": "Pentora Ghana",
            "alternateName": ["Pentora", "Pentora Education", "Mentora", "Mentora Learn"],
            "url": self.site_url,
            "logo": f"{self.site_url}/static/images/logo.png",
            "description": "Ghana's official #1 online education platform providing free quality education, BECE preparation, WASSCE preparation, and comprehensive learning materials for all students.",
            "foundingDate": "2024",
            "foundingLocation": {
                "@type": "Place",
                "name": "Ghana",
                "addressCountry": "GH"
            },
            "areaServed": {
                "@type": "Country",
                "name": "Ghana"
            },
            "audience": {
                "@type": "EducationalAudience",
                "educationalRole": "student"
            },
            "sameAs": [
                "https://facebook.com/PentoraGhana",
                "https://twitter.com/PentoraGhana",
                "https://instagram.com/PentoraGhana",
                "https://linkedin.com/company/pentora-ghana",
                "https://youtube.com/@PentoraGhana"
            ],
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+233-505-584-553",
                "contactType": "customer service",
                "availableLanguage": ["English"],
                "areaServed": "GH"
            },
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "Ghana",
                "addressRegion": "Greater Accra"
            },
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "name": "Ghana Education Service Approved",
                "description": "Approved educational content provider"
            }
        }
        return json.dumps(schema, indent=2)
    
    def _generate_course_schema(self, data):
        """Generate Course schema"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": data.get('name'),
            "description": data.get('description'),
            "provider": {
                "@type": "Organization",
                "name": self.site_name,
                "url": self.site_url
            },
            "educationalLevel": data.get('level', 'Beginner'),
            "courseCode": data.get('code'),
            "hasCourseInstance": {
                "@type": "CourseInstance",
                "courseMode": "online",
                "instructor": {
                    "@type": "Person",
                    "name": "Pentora Team"
                }
            }
        }
        return json.dumps(schema, indent=2)
    
    def _generate_quiz_schema(self, data):
        """Generate Quiz/Exercise schema"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Quiz",
            "name": data.get('name'),
            "description": data.get('description'),
            "educationalLevel": data.get('level'),
            "learningResourceType": "Quiz",
            "interactivityType": "active",
            "isAccessibleForFree": True,
            "inLanguage": "en",
            "provider": {
                "@type": "Organization",
                "name": self.site_name
            }
        }
        return json.dumps(schema, indent=2)
    
    def _generate_article_schema(self, data):
        """Generate Article schema for study notes"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": data.get('title'),
            "description": data.get('description'),
            "author": {
                "@type": "Organization",
                "name": self.site_name
            },
            "publisher": {
                "@type": "Organization",
                "name": self.site_name,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{self.site_url}/static/images/logo.png"
                }
            },
            "datePublished": data.get('created_at'),
            "dateModified": data.get('updated_at'),
            "mainEntityOfPage": data.get('url'),
            "image": data.get('image', f"{self.site_url}/static/images/default-article.jpg")
        }
        return json.dumps(schema, indent=2)
    
    def _generate_breadcrumb_schema(self, breadcrumbs):
        """Generate BreadcrumbList schema"""
        items = []
        for i, crumb in enumerate(breadcrumbs, 1):
            items.append({
                "@type": "ListItem",
                "position": i,
                "name": crumb['name'],
                "item": crumb['url']
            })
        
        schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": items
        }
        return json.dumps(schema, indent=2)


def generate_sitemap_urls():
    """
    Generate URLs for sitemap
    """
    from subjects.models import Subject, ClassLevel, Topic
    from django.urls import reverse
    
    urls = []
    
    # Static pages
    static_pages = [
        ('core:home', 1.0, 'daily'),
        ('subjects:list', 0.9, 'weekly'),
        ('subjects:simple_learn', 0.9, 'weekly'),
        ('subjects:quiz_list', 0.8, 'weekly'),
        ('core:about', 0.6, 'monthly'),
        ('core:contact', 0.6, 'monthly'),
        ('core:help', 0.7, 'monthly'),
    ]
    
    for url_name, priority, changefreq in static_pages:
        try:
            urls.append({
                'location': reverse(url_name),
                'priority': priority,
                'changefreq': changefreq
            })
        except:
            pass
    
    # Subject pages
    for subject in Subject.objects.filter(is_active=True):
        urls.append({
            'location': reverse('subjects:detail', args=[subject.slug]),
            'priority': 0.8,
            'changefreq': 'weekly'
        })
        
        # Class level pages
        for class_level in subject.get_class_levels():
            urls.append({
                'location': reverse('subjects:class_detail', args=[subject.slug, class_level.level_number]),
                'priority': 0.7,
                'changefreq': 'weekly'
            })
            
            # Topic pages
            for topic in class_level.topics.filter(is_active=True):
                urls.append({
                    'location': reverse('subjects:topic_detail', args=[subject.slug, class_level.level_number, topic.slug]),
                    'priority': 0.6,
                    'changefreq': 'weekly'
                })
    
    return urls


def generate_robots_txt():
    """
    Generate robots.txt content
    """
    content = """User-agent: *
Allow: /

# Sitemaps
Sitemap: {}/sitemap.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /api/
Disallow: /media/private/
Disallow: /dashboard/
Disallow: /profile/

# Allow important pages
Allow: /subjects/
Allow: /quiz/
Allow: /static/

# Crawl delay
Crawl-delay: 1
""".format(settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'https://Pentora.com')
    
    return content


class MetaTagsHelper:
    """
    Helper class for generating meta tags in templates
    """
    
    @staticmethod
    def subject_meta(subject):
        """Generate meta tags for subject pages"""
        return {
            'title': f"{subject.name} - Free Online Learning | Pentora",
            'description': f"Learn {subject.name} with free interactive lessons, quizzes, and study materials. Perfect for students of all grades.",
            'keywords': f"{subject.name.lower()}, online learning, free education, study materials, quizzes",
        }
    
    @staticmethod
    def topic_meta(topic):
        """Generate meta tags for topic pages"""
        return {
            'title': f"{topic.title} - {topic.class_level.subject.name} | Pentora",
            'description': f"Master {topic.title} with comprehensive study notes, practice quizzes, and interactive learning materials.",
            'keywords': f"{topic.title.lower()}, {topic.class_level.subject.name.lower()}, grade {topic.class_level.level_number}",
        }
    
    @staticmethod
    def quiz_meta(quiz_type, subject=None, topic=None):
        """Generate meta tags for quiz pages"""
        if topic:
            title = f"{topic.title} Quiz - {subject.name} | Pentora"
            description = f"Test your knowledge of {topic.title} with our interactive quiz. Get instant feedback and improve your understanding."
        elif subject:
            title = f"{subject.name} Quizzes - Practice Tests | Pentora"
            description = f"Practice {subject.name} with our comprehensive collection of quizzes and tests for all grade levels."
        else:
            title = "Free Online Quizzes - All Subjects | Pentora"
            description = "Access thousands of free practice quizzes across all subjects and grade levels. Test your knowledge and track your progress."
        
        return {
            'title': title,
            'description': description,
            'keywords': f"quiz, practice test, {subject.name.lower() if subject else 'online learning'}, free education",
        }
