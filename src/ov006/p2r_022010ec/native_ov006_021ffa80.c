#include "context.h"

/* Stop the stream the block points at and clear its pending word. */
void native_ov006_021ffa80(s32 arg)
{
    native_fn_02204974(0, arg);
    *(s32 *)(*(u8 **)(native_data_ov006_0221c150 + 4) + 0x14) = 0;
}
