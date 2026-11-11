#include "context.h"

/* Retire the three resource queues the frame decoder opened and forward the
   argument to the decoder registered for the current stream entry. */
void native_ov006_022074c0(s32 arg)
{
    native_fn_0205f9e4(native_data_ov006_0221c2c0);
    native_fn_0205f9e4(native_data_ov006_0221c350);
    native_fn_0205f9e4(native_data_ov006_0221c308);
    (*(void (**)(s32))(native_data_ov006_0220bc24
                       + *(s32 *)(native_data_ov006_0221c27c + 0x08) * 4))(arg);
}
