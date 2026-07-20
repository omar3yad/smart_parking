"""
core/sse.py
منطق عام لأي SSE endpoint في المشروع: بيعمل subscribe على قناة/قنوات Redis
ويحوّل الرسائل لصيغة SSE، مع keep-alive عشان الاتصال ميتقفلش من الـ proxy/browser.
"""
import json
from django.http import StreamingHttpResponse
from core.redis_client import get_redis_connection

KEEPALIVE_INTERVAL = 15  # ثانية — نبعت comment فاضي عشان نفضل الاتصال حي


def sse_format(event_type: str, data: dict) -> str:
    """يبني رسالة SSE صحيحة الصيغة."""
    return f"event: {event_type}\ndata: {json.dumps(data, default=str)}\n\n"


def event_stream(channels: list[str]):
    """
    Generator بيعمل subscribe على قناة أو أكتر ويـ yield كل رسالة توصل.
    بيستخدم get_message مع timeout بدل listen() العادية عشان نقدر نبعت keep-alive.
    """
    conn = get_redis_connection()
    pubsub = conn.pubsub()
    pubsub.subscribe(*channels)

    try:
        # أول رسالة بتكون تأكيد الاشتراك من Redis نفسه — نتجاهلها
        for message in pubsub.listen():
            break

        while True:
            message = pubsub.get_message(timeout=KEEPALIVE_INTERVAL)
            if message is None:
                # مفيش حدث جديد خلال الفترة دي → ابعت keep-alive عشان الاتصال يفضل مفتوح
                yield ": keep-alive\n\n"
                continue

            if message.get('type') != 'message':
                continue

            try:
                payload = json.loads(message['data'])
            except (TypeError, ValueError):
                continue

            yield sse_format(payload.get('event', 'message'), payload.get('data', {}))
    finally:
        pubsub.unsubscribe(*channels)
        pubsub.close()


def make_sse_response(channels: list[str]) -> StreamingHttpResponse:
    response = StreamingHttpResponse(
        event_stream(channels),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # مهم جدًا لو Nginx قدام Gunicorn — يمنع الـ buffering
    return response