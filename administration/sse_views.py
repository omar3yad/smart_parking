"""
administration/sse_views.py
Endpoint الـ SSE الخاص بالداشبورد — بيستقبل كل الأحداث (دخول + خروج + دفع).
"""
from django.contrib.auth.decorators import login_required
from core.sse import make_sse_response


@login_required
def dashboard_stream(request):
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Admins only.")
    return make_sse_response(['parking:entry', 'parking:exit', 'parking:payment'])