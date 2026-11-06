#include "context_00.h"
#include "msl_arm_varargs.h"
WMErrCode native_main_020118a4 (WMApiid id, u16 paramNum, ...)
{
    va_list vlist;
    s32 i;
    int result;
    u32 * tmpAddr;
    ((void) 0) ;
    tmpAddr = native_fn_0201184c();
    if (tmpAddr == ((void *)0) ) {
        return WM_ERRCODE_FIFO_ERROR;
    }
    *(u16 *)tmpAddr = (u16)id;
    va_start(vlist, paramNum);
    for (i = 0; i < paramNum; i++) {
        tmpAddr[i + 1] = va_arg(vlist, u32) ;
    }
    ((void)0) ;
    native_fn_020072ec(tmpAddr, 256 );
    result = native_fn_0200a440(PXI_FIFO_TAG_WM, (u32)tmpAddr, 0 );
    (void)native_fn_02006e24(&native_data_main_020e5d80.field_0008, tmpAddr, 1 );
    if (result < 0) {
        ((void) 0) ;
        return WM_ERRCODE_FIFO_ERROR;
    }
    return WM_ERRCODE_OPERATING;
}
