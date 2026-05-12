# handlers/__init__.py
from .start import register_handlers
from .group_commands import register_group_commands   # نشط مرة أخرى
from .repo import register_repo_handler

# ── R3D feature plugins (auto-register via @app.on_message decorators) ──
from . import customCommad
from . import customRank
from . import del_ranks
from . import get_ranks
from . import globalFilters
from . import mute_and_gban
from . import sarhni
from . import set_ranks

def register_all_handlers(app):
    register_handlers(app)
    register_repo_handler(app)
    register_group_commands(app)   # استدعاء تفعيل أوامر المجموعات
    print("✅ Core handlers registered!")
    print("✅ R3D feature plugins loaded!")
