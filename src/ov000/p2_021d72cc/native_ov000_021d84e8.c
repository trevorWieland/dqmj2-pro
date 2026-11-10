#include "context.h"

s32 native_ov000_021d84e8(s32 value, s32 mode)
{
    s32 previous = native_data_ov000_0223033c.field_4c;
    s32 result = native_fn_02028158(value);

    native_data_ov000_0223033c.field_98 = result;
    if (mode == 0)
        native_data_ov000_0223033c.field_4c = native_fn_02028158(native_data_ov000_0223033c.field_4c);
    else
        native_data_ov000_0223033c.field_4c = result;
    return previous;
}
