#include "context.h"
u32 native_ov006_021f5870(void) {
    u32 temp_r0;

    native_fn_ov006_021fed84();
    native_fn_ov006_021f5394();
    native_fn_ov006_021f2920();
    native_fn_ov006_021f2a74();
    native_fn_ov006_021f26e4();
    if ((native_fn_ov006_021f5328() == 1) && (native_fn_ov006_021f5344(2) != 0)) {
        *(u32 *)native_data_ov006_0221c098 = native_fn_ov006_021f53c8(native_data_ov006_0220da80);
    } else {
        *(u32 *)native_data_ov006_0221c098 = native_fn_ov006_021f53c8(*(u32 *)(native_data_ov006_0220da64 + (native_fn_ov006_021f5328() * 4)));
    }
    native_fn_ov006_02202fb8(1, native_fn_ov006_021f2798(native_data_ov006_0220da90));
    native_fn_ov006_02202fb8(0, native_fn_ov006_021f2798(native_data_ov006_0220daa4));
    native_fn_ov006_021f27d4(native_data_ov006_0220dab8, native_fn_02004f78);
    native_fn_ov006_021f27d4(native_data_ov006_0220dacc, native_fn_020048f4);
    native_fn_ov006_021f27d4(native_data_ov006_0220dae0, native_fn_02004b00);
    native_fn_ov006_021f27d4(native_data_ov006_0220daf8, native_fn_020049a4);
    native_fn_ov006_021f27d4(native_data_ov006_0220db10, native_fn_02004fd8);
    native_fn_ov006_021f27d4(native_data_ov006_0220db28, native_fn_020048a0);
    native_fn_ov006_021f27d4(native_data_ov006_0220db40, native_fn_02004aa8);
    native_fn_ov006_021f27d4(native_data_ov006_0220db58, native_fn_0200494c);
    temp_r0 = native_fn_ov006_021f5334();
    switch (temp_r0) {
    case 0:
        native_fn_ov006_021f27d4(native_data_ov006_0220db70, native_fn_02004c78);
        break;
    case 1:
        native_fn_ov006_021f27d4(native_data_ov006_0220db84, native_fn_02004c78);
        break;
    }
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 3;
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & ~3) | 3;
    *(u16 *)0x0400000A = (*(u16 *)0x0400000A & ~3) | 3;
    native_fn_ov006_02203908(1, 2);
    native_fn_ov006_02203908(0, 2);
    return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f59d8);
}
