import qualify_arm9_thumb_reference_inputs_20261105 as original
from auth_context_route_v2_20261106 import validation_route as auth_route
from embedded_reference_link_context_v2_20261106 import validation_route as embedded_route


if __name__ == '__main__':
    with auth_route(), embedded_route():
        original.main()
