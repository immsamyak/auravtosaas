from django.views.generic import ListView
from apps.admin.mixins import SuperUserRequiredMixin
from apps.fitting.models import VirtualTryOn

class VTOQueueDashboardView(SuperUserRequiredMixin, ListView):
    model = VirtualTryOn
    template_name = 'admin/vto_queue.html'
    context_object_name = 'jobs'
    paginate_by = 50

    def get_queryset(self):
        # Return all jobs, ordered by created_at descending
        return VirtualTryOn.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate queue stats
        qs = VirtualTryOn.objects.all()
        context['total_processing'] = qs.filter(status='PROCESSING').count()
        context['total_pending'] = qs.filter(status='PENDING').count()
        context['total_failed'] = qs.filter(status='FAILED').count()
        context['total_completed'] = qs.filter(status='COMPLETED').count()
        
        return context

class QAModerationView(SuperUserRequiredMixin, ListView):
    model = VirtualTryOn
    template_name = 'admin/qa_moderation.html'
    context_object_name = 'jobs'
    paginate_by = 50

    def get_queryset(self):
        # QA should moderate COMPLETED jobs that are UNREVIEWED
        return VirtualTryOn.objects.filter(status='COMPLETED', qa_status__in=['UNREVIEWED', 'FLAGGED']).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = VirtualTryOn.objects.all()
        context['qa_pending'] = qs.filter(qa_status__in=['UNREVIEWED', 'FLAGGED']).count()
        context['qa_approved'] = qs.filter(qa_status='APPROVED').count()
        context['qa_rejected'] = qs.filter(qa_status='REJECTED').count()
        return context

from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

class QAModerationActionView(SuperUserRequiredMixin, View):
    def post(self, request, pk, action):
        job = get_object_or_404(VirtualTryOn, pk=pk)
        if action == 'approve':
            job.qa_status = 'APPROVED'
            messages.success(request, f"Job #{job.id} approved.")
        elif action == 'reject':
            job.qa_status = 'REJECTED'
            messages.success(request, f"Job #{job.id} rejected.")
        else:
            messages.error(request, "Invalid action.")
            return redirect('admin:qa_moderation')
            
        job.qa_reviewed_by = request.user
        job.qa_reviewed_at = timezone.now()
        job.qa_notes = request.POST.get('qa_notes', '')
        job.save()
        
        return redirect('admin:qa_moderation')
