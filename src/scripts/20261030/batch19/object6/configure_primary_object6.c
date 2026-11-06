#include "scr_runtime_configuration.h"
void configure_primary_object6(void)
{
    shared_parameter_first = dispatch_argument0;
    shared_parameter_second = dispatch_argument1;
    shared_parameter_third = dispatch_argument2;
    shared_parameter_fourth = dispatch_argument3;
    configured_primary_6 = dispatch_argument4;
    configured_primary_6 = get_primary_flag(configured_primary_6);
    if (configured_primary_6 == false) {
        configure_runtime_object(object_category, shared_parameter_first, shared_parameter_second, shared_parameter_third, shared_parameter_fourth, 0, -1);
    } else {
        {
            configure_runtime_object(object_category, shared_parameter_first, shared_parameter_second, shared_parameter_third, shared_parameter_fourth, 2, -1);
        }
    }
}
