#include "context_00.h"
int native_main_02018828 (const void * buf, int len, int pollbmp)
{
    int errcode;
    u16 size = (u16)len;
    u16 pollbitmap = (u16)pollbmp;
    if ((native_data_main_020ec360.field_0008->mpStarted == 0) || (native_data_main_020ec360.field_0008->endReq == 1)) {
        return WM_ERRCODE_FAILED;
    }
    switch (native_data_main_020ec360.field_0008->mode) {
    case 1 :
        errcode = native_fn_020187dc(native_data_main_020ec360.field_0008->callback_ptr, (u16 *)buf, size,
                                (u16)((!native_data_main_020ec360.field_0008->contSend) ? 1000 : 0), pollbitmap);
        if (errcode == WM_ERRCODE_OPERATING) {
            native_data_main_020ec360.field_0008->mpBusy = 1;
        }
        return conv_errcode(errcode);
    case 2 :
        errcode = native_fn_020187dc(native_fn_020176d0, (u16 *)buf, size, 0, pollbitmap);
        if (errcode == WM_ERRCODE_OPERATING) {
            native_data_main_020ec360.field_0008->mpBusy = 1;
        }
        return conv_errcode(errcode);
    default:
        return WM_ERRCODE_FAILED;
    }
}
