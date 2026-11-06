#include "context_00.h"
#include "msl_arm_varargs.h"
WMErrCode native_main_02011a34 (s32 paramNum, ...)
{
    WMErrCode result;
    u16 now;
    u32 temp;
    va_list vlist;
    result = native_fn_020119d0();
    if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    native_fn_020072d0(&(native_data_main_020e5d80.field_0004->status->state), 2);
    now = native_data_main_020e5d80.field_0004->status->state;
    result = WM_ERRCODE_ILLEGAL_STATE;
    va_start(vlist, paramNum);
    for (; paramNum; paramNum--) {
        temp = va_arg(vlist, u32) ;
        if (temp == now) {
            result = WM_ERRCODE_SUCCESS;
        }
    }
    ((void)0) ;
    if (result == WM_ERRCODE_ILLEGAL_STATE) {
        ((void) 0) ;
    }
    return result;
}
