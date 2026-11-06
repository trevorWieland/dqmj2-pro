#include "context.h"
u32 native_main_0202a8e0(u32 path) {
    u32 file[18];
    u32 length = 0;
    native_fn_0200bd04(file);
    if (native_fn_0200bfe4(file,path)) {
        length = file[10] - file[9];
        if (length != 0) {
            native_data_020edec8 = 0;
        } else {
            native_data_020edec8 = 3;
        }
        native_fn_0200c02c(file);
    } else {
        native_data_020edec8 = 1;
    }
    return length;
}
