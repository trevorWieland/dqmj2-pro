#include "context.h"

/* Look the registered device block up and hand the caller the stored geometry:
   returns 2 when the caller asked for no rewrite, 1 when a block was written,
   0 when no device is registered or the lookup found nothing. */
s32 native_ov000_021dd440(s32 arg0, s32 arg1, ParameterBlock *out)
{
    s32 result = 0;
    ParameterBlock block;
    ParameterBlock resolved;

    if (native_data_ov000_0223142c.field_79c != 0
        && native_fn_ov000_021dd1e4(arg0,
            native_data_ov000_0223142c.field_79c->field_190, &block) != 0) {
        if (arg1 == 0) {
            result = 2;
        } else {
            native_fn_ov000_021dd2a4(arg0, &block, arg1, &resolved);
            *out = resolved;
            result = 1;
        }
    }
    return result;
}
