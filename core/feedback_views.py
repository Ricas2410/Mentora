from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import UserFeedback
import json


@method_decorator(staff_member_required, name='dispatch')
class FeedbackListView(ListView):
    """Admin view to list all feedback"""
    model = UserFeedback
    template_name = 'admin/feedback/list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = UserFeedback.objects.select_related('user').order_by('-created_at')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status == 'resolved':
            queryset = queryset.filter(is_resolved=True)
        elif status == 'unresolved':
            queryset = queryset.filter(is_resolved=False)
        
        # Filter by type
        feedback_type = self.request.GET.get('type')
        if feedback_type:
            queryset = queryset.filter(feedback_type=feedback_type)
        
        # Filter by rating
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(message__icontains=search) |
                Q(user__email__icontains=search) |
                Q(email__icontains=search) |
                Q(page_url__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        total_feedback = UserFeedback.objects.count()
        resolved_feedback = UserFeedback.objects.filter(is_resolved=True).count()
        unresolved_feedback = total_feedback - resolved_feedback
        
        # Average rating
        avg_rating = UserFeedback.objects.filter(rating__isnull=False).aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        
        # Feedback by type
        feedback_by_type = UserFeedback.objects.values('feedback_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Recent feedback (last 7 days)
        from datetime import datetime, timedelta
        from django.utils import timezone
        week_ago = timezone.now() - timedelta(days=7)
        recent_feedback = UserFeedback.objects.filter(created_at__gte=week_ago).count()
        
        context.update({
            'total_feedback': total_feedback,
            'resolved_feedback': resolved_feedback,
            'unresolved_feedback': unresolved_feedback,
            'avg_rating': round(avg_rating, 1),
            'feedback_by_type': feedback_by_type,
            'recent_feedback': recent_feedback,
            'current_filters': {
                'status': self.request.GET.get('status', ''),
                'type': self.request.GET.get('type', ''),
                'rating': self.request.GET.get('rating', ''),
                'search': self.request.GET.get('search', ''),
            }
        })
        
        return context


@method_decorator(staff_member_required, name='dispatch')
class FeedbackDetailView(DetailView):
    """Admin view to view individual feedback"""
    model = UserFeedback
    template_name = 'admin/feedback/detail.html'
    context_object_name = 'feedback'
    pk_url_kwarg = 'feedback_id'


@staff_member_required
@require_http_methods(["POST"])
def update_feedback_status(request, feedback_id):
    """Update feedback resolution status"""
    feedback = get_object_or_404(UserFeedback, id=feedback_id)
    
    action = request.POST.get('action')
    admin_notes = request.POST.get('admin_notes', '')
    
    if action == 'resolve':
        feedback.is_resolved = True
        feedback.admin_notes = admin_notes
        feedback.save()
        messages.success(request, 'Feedback marked as resolved.')
    elif action == 'unresolve':
        feedback.is_resolved = False
        feedback.save()
        messages.success(request, 'Feedback marked as unresolved.')
    elif action == 'update_notes':
        feedback.admin_notes = admin_notes
        feedback.save()
        messages.success(request, 'Admin notes updated.')
    
    return redirect('core:feedback_detail', feedback_id=feedback_id)


@staff_member_required
@csrf_exempt
@require_http_methods(["POST"])
def bulk_feedback_action(request):
    """Handle bulk actions on feedback"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        feedback_ids = data.get('feedback_ids', [])
        
        if not feedback_ids:
            return JsonResponse({'success': False, 'message': 'No feedback selected'})
        
        feedbacks = UserFeedback.objects.filter(id__in=feedback_ids)
        
        if action == 'resolve':
            feedbacks.update(is_resolved=True)
            message = f'{feedbacks.count()} feedback(s) marked as resolved'
        elif action == 'unresolve':
            feedbacks.update(is_resolved=False)
            message = f'{feedbacks.count()} feedback(s) marked as unresolved'
        elif action == 'delete':
            count = feedbacks.count()
            feedbacks.delete()
            message = f'{count} feedback(s) deleted'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'})
        
        return JsonResponse({'success': True, 'message': message})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@staff_member_required
def feedback_analytics(request):
    """Feedback analytics dashboard"""
    from django.db.models import Count, Avg
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Time periods
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic stats
    total_feedback = UserFeedback.objects.count()
    resolved_feedback = UserFeedback.objects.filter(is_resolved=True).count()
    avg_rating = UserFeedback.objects.filter(rating__isnull=False).aggregate(
        avg=Avg('rating')
    )['avg'] or 0
    
    # Feedback over time (last 30 days)
    feedback_over_time = []
    for i in range(30):
        date = today - timedelta(days=29-i)
        count = UserFeedback.objects.filter(created_at__date=date).count()
        feedback_over_time.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Feedback by type
    feedback_by_type = UserFeedback.objects.values('feedback_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Rating distribution
    rating_distribution = UserFeedback.objects.filter(rating__isnull=False).values('rating').annotate(
        count=Count('id')
    ).order_by('rating')
    
    # Top issues (unresolved feedback)
    top_issues = UserFeedback.objects.filter(
        is_resolved=False,
        feedback_type='bug_report'
    ).order_by('-created_at')[:10]
    
    context = {
        'total_feedback': total_feedback,
        'resolved_feedback': resolved_feedback,
        'unresolved_feedback': total_feedback - resolved_feedback,
        'avg_rating': round(avg_rating, 1),
        'feedback_over_time': feedback_over_time,
        'feedback_by_type': feedback_by_type,
        'rating_distribution': rating_distribution,
        'top_issues': top_issues,
        'recent_feedback': UserFeedback.objects.filter(
            created_at__gte=week_ago
        ).count(),
    }
    
    return render(request, 'admin/feedback/analytics.html', context)
