#include "context.h"
u32 native_main_020d2e68(void)
{
    u16 descriptor[16];
    Vec2 position = {0};
    void *formatter = native_data_021c9698;
    u16 i;
    u32 value;
    i = 0;
    do {
        native_fn_02049f4c(native_fn_02061dcc((s8)(i + 6)));
        ++i;
    } while (i < 22);
    i = 0;
    do {
        native_fn_02049ffc((*native_fn_02061dcc((s8)(i + 6)))->content4);
        ++i;
    } while (i < 22);
    native_fn_02046af4(formatter, native_data_021d70a4, 16, 0, descriptor, 255);
    native_fn_0204ab98(6, &position, 1, descriptor, 0);
    native_fn_0204aaf0(8, &position, 15, 12, 16, 1, 0);
    native_fn_0204aaf0(7, &position, 15, 15, native_data_021d7098.value22, 1, 1);
    native_fn_0204aaf0(15, &position, 15, 12, 20, 1, 0);
    value = native_data_021d7098.value34;
    if (value == 0) native_fn_0204aaf0(16, &position, 15, 2, 122, 1, 1);
    else {
        if (value > 99999) value = 99999;
        native_fn_02048094(value, 0);
        native_fn_0204aaf0(16, &position, 15, 12, 22, 1, 1);
    }
    native_fn_0204aaf0(9, &position, 15, 12, 17, 1, 0);
    value = native_data_021d7098.value28;
    if (value == 0) native_fn_0204aaf0(10, &position, 15, 2, 122, 1, 1);
    else {
        if (value > 99999) value = 99999;
        native_fn_02048094(value, 0);
        native_fn_0204aaf0(10, &position, 15, 12, 22, 1, 1);
    }
    native_fn_0204aaf0(11, &position, 15, 12, 18, 1, 0);
    value = native_data_021d7098.value2C;
    if (value == 0) native_fn_0204aaf0(12, &position, 15, 2, 122, 1, 1);
    else {
        if (value > 99999) value = 99999;
        native_fn_02048094(value, 0);
        native_fn_0204aaf0(12, &position, 15, 12, 22, 1, 1);
    }
    native_fn_0204aaf0(13, &position, 15, 12, 19, 1, 0);
    value = native_data_021d7098.value30;
    if (value == 0) native_fn_0204aaf0(14, &position, 15, 2, 122, 1, 1);
    else {
        if (value > 99999) value = 99999;
        native_fn_02048094(value, 0);
        native_fn_0204aaf0(14, &position, 15, 12, 22, 1, 1);
    }
    native_fn_0204aaf0(17, &position, 15, 12, 23, 1, 0);
    value = native_data_021d7098.packed38.low0;
    if (value > 999) value = 999;
    native_fn_02048094(value, 0);
    native_fn_0204aaf0(18, &position, 15, 12, 13, 1, 1);
    value = native_data_021d7098.packed38.middle10;
    if (value > 999) value = 999;
    native_fn_02048094(value, 0);
    native_fn_0204aaf0(19, &position, 15, 12, 14, 1, 1);
    native_fn_0204aaf0(20, &position, 15, 12, 24, 1, 0);
    value = native_data_021d7098.packed3C.low0;
    if (value > 999) value = 999;
    native_fn_02048094(value, 0);
    native_fn_0204aaf0(21, &position, 15, 12, 13, 1, 1);
    native_fn_0204aaf0(22, &position, 15, 12, 25, 1, 0);
    value = native_data_021d7098.packed38.high20;
    if (value > 999) value = 999;
    native_fn_02048094(value, 0);
    native_fn_0204aaf0(23, &position, 15, 12, 15, 1, 1);
    native_fn_0204aaf0(24, &position, 15, 12, 26, 1, 1);
    native_fn_020d28cc(25, native_data_021d7098.value24);
    native_fn_0204aaf0(26, &position, 15, 12, 27, 1, 1);
    return native_fn_020d2a14(27, native_data_021d7098.value20);
}
