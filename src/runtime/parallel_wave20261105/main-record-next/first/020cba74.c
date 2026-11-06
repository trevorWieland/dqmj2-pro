#include "context.h"

NativeState* native_main_020cba74(void) {
    s8 first = 6;
    s8 second = 8;
    s8 third = 6;
    u8 index = 0;
    do {
        native_fn_020cb42c(index);
        native_data_021d6620.field0000 += native_fn_020cb5c4(index,&first,&second,&third);
        if(native_data_021d6630.field00d1.bit3) {
            native_data_021d6630.field00d1.bit3 = 0;
            native_fn_020cb2fc();
            break;
        }
        index += 1;
    } while(index < 3);
    native_data_021d6630.field00d1.bit2 = 0;
    native_data_021d6630.field00d1.bit1 = -1;
    return &native_data_021d6630;
}
