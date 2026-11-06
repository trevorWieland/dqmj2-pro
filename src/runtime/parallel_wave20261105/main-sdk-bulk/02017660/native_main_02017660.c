#include "context_00.h"
void native_main_02017660 (void * arg)
{
    WMPortRecvCallback * cb = (WMPortRecvCallback *)arg;
    if (cb->errcode != WM_ERRCODE_SUCCESS) {
        return;
    }
    switch (cb->state) {
    case WM_STATECODE_PORT_RECV:
        native_data_main_020ec360.field_0008->callback(9 , (void *)(arg));
        break;
    case WM_STATECODE_CONNECTED:
        break;
    case WM_STATECODE_PORT_INIT:
    case WM_STATECODE_DISCONNECTED:
    case WM_STATECODE_DISCONNECTED_FROM_MYSELF:
        break;
    }
}
