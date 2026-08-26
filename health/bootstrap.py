import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_app():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    root_s = str(root)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
    spec = spec_from_file_location("mashuk_forms_app", root / "app.py")
    mod = module_from_spec(spec)
    sys.modules["mashuk_forms_app"] = mod
    spec.loader.exec_module(mod)
    return mod.app
