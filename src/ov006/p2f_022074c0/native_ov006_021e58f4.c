#include "context.h"

/* Open the two sound work buffers and hand the resulting mixer state to the
   channel table, then publish the new sound block. */
void native_ov006_021e58f4(void)
{
    u8 params[0x10];
    u8 state[0x24];

    native_fn_ov006_021e3cd4();
    native_fn_02008d78(params, 0, 0x10);
    native_fn_02008d78(state, 0, 0x24);
    native_fn_ov006_021e7a60(0, native_fn_ov006_021e5870(0x24, state, 0x10,
                                                        native_fn_020baf04(params)));
    native_fn_ov006_021e7d98(0);
    native_fn_ov006_021e9148(native_data_ov006_02207db8, 1);
}
