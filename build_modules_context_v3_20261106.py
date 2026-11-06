import build_modules as original
from auth_context_route_v2_20261106 import module_route
from build_lock import accepted_build


if __name__ == '__main__':
    with accepted_build(), module_route(original):
        raise SystemExit(original.main())
