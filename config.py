import os
from dotenv import load_dotenv

load_dotenv()

# â”€â”€ Telegram API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
API_ID       = int(os.getenv("API_ID", 0))
API_HASH     = os.getenv("API_HASH", "")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")

# â”€â”€ MongoDB (existing features) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
MONGO_URI    = os.getenv("MONGO_URI", "")
DB_NAME      = os.getenv("DB_NAME", "Cluster0")

# â”€â”€ Owner / Bot Info â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
OWNER_ID     = int(os.getenv("OWNER_ID", 0))
BOT_USERNAME = os.getenv("BOT_USERNAME", "NomadeHelpBot")
botUsername  = BOT_USERNAME   # alias used by R3D plugins

# â”€â”€ Links & Visuals â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SUPPORT_GROUP  = os.getenv("SUPPORT_GROUP",  "https://t.me/LearningBotsCommunity")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/Learning_Bots")
START_IMAGE    = os.getenv("START_IMAGE",    "https://files.catbox.moe/o5eekb.jpg")

# â”€â”€ R3D developer ID â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Dev_Zaid = os.getenv("DEV_ZAID", str(OWNER_ID))

# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ
# Redis â€” supports both Upstash REST and standard Redis
# Priority:
#   1. Upstash REST (UPSTASH_REDIS_REST_URL + TOKEN)
#   2. Standard Redis (REDIS_URL)
#   3. Fallback dummy (no Redis â€” R3D features won't work)
# â•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گâ•گ

UPSTASH_URL   = os.getenv("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN", "")
REDIS_URL     = os.getenv("REDIS_URL", "")

if UPSTASH_URL and UPSTASH_TOKEN:
    # Upstash REST (recommended for Render / cloud hosting)
    try:
        from upstash_redis import Redis as _UpstashRedis
        r = _UpstashRedis(url=UPSTASH_URL, token=UPSTASH_TOKEN)
        r.ping()
        print("âœ… Redis connected via Upstash REST")
    except Exception as e:
        print(f"âڑ ï¸ڈ  Upstash connection failed: {e}")
        r = None

elif REDIS_URL:
    # Standard Redis TCP (local or RedisLabs etc.)
    try:
        import redis as _redis
        r = _redis.from_url(REDIS_URL, decode_responses=True)
        r.ping()
        print("âœ… Redis connected via standard client")
    except Exception as e:
        print(f"âڑ ï¸ڈ  Redis connection failed: {e}")
        r = None

else:
    r = None

# If Redis unavailable, use a no-op fallback so bot doesn't crash
if r is None:
    print("âڑ ï¸ڈ  Redis not configured â€” R3D features will be disabled")
    class _FakeRedis:
        def get(self, *a, **kw):    return None
        def set(self, *a, **kw):    return None
        def delete(self, *a, **kw): return None
        def smembers(self, *a, **kw): return set()
        def sadd(self, *a, **kw):   return None
        def srem(self, *a, **kw):   return None
        def ping(self):             return True
        def lrange(self, *a, **kw): return []
        def rpush(self, *a, **kw):  return None
        def llen(self, *a, **kw):   return 0
        def expire(self, *a, **kw): return None
        def exists(self, *a, **kw): return False
        def incr(self, *a, **kw):   return 0
        def keys(self, *a, **kw):   return []
        def incrby(self, *a, **kw): return 0
    r = _FakeRedis()
