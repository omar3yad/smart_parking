"""
parking/sse_views.py
Endpoints الـ SSE الخاصة ببوابة الدخول والخروج.
"""
from django.contrib.auth.decorators import login_required
from core.sse import make_sse_response


@login_required
def entry_gate_stream(request):
    """بث لحظي لأحداث الدخول فقط — تستخدمه entry_gate.html"""
    return make_sse_response(['parking:entry'])


@login_required
def exit_gate_stream(request):
    """بث لحظي لأحداث الخروج وتأكيد الدفع — تستخدمه exit_gate.html"""
    return make_sse_response(['parking:exit', 'parking:payment'])