#include "../context.h"

/* 0x021f8dcc: run the selection handler and reset the byte it reports on. */
u32 native_ov001_021f8dcc(void) {
    u32 flag = native_data_ov001_0223989c[0x35] == 1;
    if (native_fn_ov001_02216ac4(*(u32 *)(native_data_ov001_0223989c + 0x84),
                                 native_data_ov001_0223989c[0x12], flag) != 0) {
        native_data_ov001_0223989c[0x1b] = 27;
    }
    return 0;
}
