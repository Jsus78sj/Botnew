# handlers/__init__.py
from .start import register_handlers
from .group_commands import register_group_commands
from .repo import register_repo_handler

# ── New R3D feature plugins (auto-register via @app.on_message decorators) ──
from . import customCommad
from . import customRank
from . import del_ranks
from . import get_ranks
from . import globalFilters
from . import id as id_handler   # 'id' is a Python builtin — aliased here
from . import mute_and_gban
from . import private_sudos
from . import sarhni
from . import set_ranks

def register_all_handlers(app):
    register_handlers(app)
    register_repo_handler(app)
    register_group_commands(app)
    print("✅ Core handlers registered!")
    print("✅ R3D feature plugins loaded!")
