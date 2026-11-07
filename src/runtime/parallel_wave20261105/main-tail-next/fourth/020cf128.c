#include "context.h"
u32 native_main_020cf128(void)
{
    u32 result = 0;
    switch (native_data_021d69b0) {
    case 1:
        native_fn_020c48bc();
        native_fn_020c48d0(9,8,43);
        native_fn_020c485c();
        native_fn_020c48e8(87);
        native_fn_020c484c(0);
        native_fn_020c4928(0,0);
        native_fn_020c48f8(3);
        native_data_021d69b0 = 2;
        result = 1;
        break;
    case 2:
        native_fn_020c48bc();
        native_fn_020c48d0(9,8,44);
        native_fn_020c485c();
        native_fn_020c48e8(87);
        native_fn_020c484c(0);
        native_fn_020c4928(0,0);
        native_fn_020c48f8(1);
        native_data_021d69b0 = 0;
        result = 1;
        break;
    }
    return result;
}
