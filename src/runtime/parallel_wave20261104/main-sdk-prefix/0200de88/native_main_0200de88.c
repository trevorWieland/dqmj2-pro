#include "context_00.h"
u32 native_main_0200de88 (TPData * result)
{
    ((void) 0) ;
    native_fn_0200e390(TP_REQUEST_COMMAND_FLAG_SAMPLING);
    if (native_data_main_020e53d0.field_0004.err_flg & TP_REQUEST_COMMAND_FLAG_SAMPLING) {
        return 1;
    }
    *result = native_data_main_020e53d0.field_0004.buf;
    return 0;
}
