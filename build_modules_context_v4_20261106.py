import build_modules as original
from auth_context_route_v2_20261106 import module_route as auth_route
from mb_register_module_route_v1_20261106 import module_route as register_route
from build_lock import accepted_build


if __name__ == '__main__':
    with accepted_build(), auth_route(original), register_route(original):
        raise SystemExit(original.main())
