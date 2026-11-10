#include "context.h"

/* Copy the caller's three-word block into the overlay's parameter mirror and
   accumulate the animated offset (0x58) into the running value (0x6c). */
ParameterBlock *native_ov000_021d8a6c(ParameterBlock *source)
{
    if (source != 0)
        native_data_ov000_022303a4 = *source;
    native_data_ov000_0223033c.field_6c =
        native_data_ov000_0223033c.field_6c + native_data_ov000_0223033c.field_58;
    return &native_data_ov000_022303a4;
}
