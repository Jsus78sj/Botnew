import os, redis
from dotenv import load_dotenv

load_dotenv()

# ── Telegram API ──────────────────────────────────
API_ID       = int(os.getenv("API_ID", 0))
API_HASH     = os.getenv("API_HASH", "")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")

# ── MongoDB (existing features) ───────────────────
MONGO_URI    = os.getenv("MONGO_URI", "")
DB_NAME      = os.getenv("DB_NAME", "Cluster0")

# ── Owner / Bot Info ──────────────────────────────
OWNER_ID     = int(os.getenv("OWNER_ID", 0))
BOT_USERNAME = os.getenv("BOT_USERNAME", "NomadeHelpBot")
botUsername  = BOT_USERNAME   # alias used by R3D plugins

# ── Links & Visuals ───────────────────────────────
SUPPORT_GROUP  = os.getenv("SUPPORT_GROUP",  "https://t.me/LearningBotsCommunity")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/Learning_Bots")
START_IMAGE    = os.getenv("START_IMAGE",    "https://files.catbox.moe/o5eekb.jpg")

# ══════════════════════════════════════════════════
# Redis (required by R3D plugins)
# Set REDIS_URL in your .env:
#   REDIS_URL=redis://localhost:6379
#   or e.g. rediss://:<password>@<host>:<port>
# ══════════════════════════════════════════════════
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    r = redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()
except Exception:
    # Fallback: dummy Redis that returns None for all ops
    class _FakeRedis:
        def get(self, *a, **kw): return None
        def set(self, *a, **kw): return None
        def delete(self, *a, **kw): return None
        def smembers(self, *a, **kw): return set()
        def sadd(self, *a, **kw): return None
        def srem(self, *a, **kw): return None
        def ping(self): return True
        def lrange(self, *a, **kw): return []
        def rpush(self, *a, **kw): return None
        def llen(self, *a, **kw): return 0
        def expire(self, *a, **kw): return None
        def exists(self, *a, **kw): return False
        def incr(self, *a, **kw): return 0
        def keys(self, *a, **kw): return []
        def incrby(self, *a, **kw): return 0
    r = _FakeRedis()

# ══════════════════════════════════════════════════
# R3D-specific config variables
# ══════════════════════════════════════════════════
# Developer / Bot Owner ID — set DEV_ZAID in .env
Dev_Zaid = os.getenv("DEV_ZAID", str(OWNER_ID))
