#include "context.h"

void native_ov006_021f5f30(void)
{
    switch (ov006_context_byte_16_021f2390()) {
    case 0:
        native_fn_ov006_021ff6d4(7);
        ov006_main_loop_set_callback_021f52cc((void (*)(void))0x021F5F79);
        return;
    case 1:
        native_fn_ov006_021ff6d4(6);
        native_fn_02200344(0x18, 0, 1, -1, 0);
        native_fn_021f23f4();
        ov006_main_loop_set_callback_021f52cc((void (*)(void))0x021F604D);
        return;
    }
}
