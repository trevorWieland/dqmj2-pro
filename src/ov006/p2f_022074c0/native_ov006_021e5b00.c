#include "context.h"

/* Open the two sound work buffers, rebuild the channel table from the resulting
   mixer state and install the second sound block. */
void native_ov006_021e5b00(void)
{
    u8 params[0x10];
    u8 state[0x24];

    ov006_noop_021e3cd4();
    native_fn_02008d78(params, 0, 0x10);
    native_fn_02008d78(state, 0, 0x24);
    native_fn_ov006_021e7a60(0, native_fn_ov006_021e5870(0x24, state, 0x10,
                                                        native_fn_020baf04(params)));
    native_fn_ov006_021e7e78(1);
    ov006_commit_mode_transition_021e9148(native_data_ov006_02207da0, 1);
}
