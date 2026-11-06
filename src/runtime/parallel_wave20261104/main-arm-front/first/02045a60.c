#include "context.h"
u32 native_main_02045a60(u32 arg0, const void *arg1, u32 arg2, u32 arg3) {
    native_fn_02007308(arg1, arg3);
    switch (arg0) {
    case 0:
        native_fn_02004bb8(arg1, arg2, arg3);
        break;
    case 1:
        native_fn_02004c78(arg1, arg2, arg3);

        break;
    case 2:
        native_fn_02004d38(arg1, arg2, arg3);

        break;
    case 3:
        native_fn_02004df8(arg1, arg2, arg3);

        break;
    default:
        native_fn_02008430();
        return 0U;
    }
    return 1U;
}
