"""
core/redis_client.py
عميل Redis واحد مشترك لكل المشروع (Singleton) — للنشر (publish) والاشتراك (subscribe).
"""
import json
import redis
from django.conf import settings

_redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_redis_connection():
    return redis.Redis(connection_pool=_redis_pool)


def publish_event(channel: str, event_type: str, data: dict):
    """
    ينشر حدث على قناة Redis معينة.
    الـ payload بيتبعت كـ JSON فيه event_type + data عشان الفرونت يقدر يميّز.
    """
    conn = get_redis_connection()
    payload = json.dumps({"event": event_type, "data": data}, default=str)
    conn.publish(channel, payload)