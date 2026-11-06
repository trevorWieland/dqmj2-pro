#include "context_00.h"
#include "context_01.h"
void native_main_02016e08 (void * arg)
{
    int errcode;
    WMCallback * buf = (WMCallback *)arg;
    switch (buf->apiid) {
    case WM_APIID_INITIALIZE:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            native_data_main_020ec360.field_0008->callback(256 , arg);
            return;
        }
        native_fn_02016d74();
    }
    break;
    case WM_APIID_SET_LIFETIME:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            native_data_main_020ec360.field_0008->callback(256 , arg);
            return;
        }
        errcode = native_fn_02012864(native_main_02016e08, &native_data_main_020ec360.field_0008->parentParam);
        native_fn_020189b0(WM_APIID_SET_P_PARAM, errcode);
    }
    break;
    case WM_APIID_SET_P_PARAM:
    {
        native_data_main_020ec360.field_0008->callback(21 , arg);
        errcode = native_fn_020141b0(native_main_02016e08, 1);
        native_fn_020189b0(WM_APIID_SET_BEACON_IND, errcode);
    }
    break;
    case WM_APIID_SET_BEACON_IND:
        if (!native_data_main_020ec360.field_0008->endReq) {
            if (buf->errcode != WM_ERRCODE_SUCCESS) {
                native_data_main_020ec360.field_0008->callback(256 , arg);
                return;
            }
            errcode = native_fn_02012990(native_main_02016e08, native_data_main_020dce94.field_000c);
            native_fn_020189b0(WM_APIID_START_PARENT, errcode);
        } else {
            if (buf->errcode != WM_ERRCODE_SUCCESS) {
                native_data_main_020ec360.field_0008->endReq = 0;
                native_data_main_020ec360.field_0008->callback(256 , arg);
            } else {
                native_fn_02016dc4(arg);
            }
        }
        break;
    case WM_APIID_START_PARENT:
    {
        WMstartParentCallback * callback = (WMstartParentCallback *)arg;
        if (callback->errcode != WM_ERRCODE_SUCCESS) {
            native_data_main_020ec360.field_0008->callback(256 , arg);
            return;
        }
        switch (callback->state) {
        case WM_STATECODE_PARENT_START:
            native_data_main_020ec360.field_0008->child_bitmap = 0;
            native_data_main_020ec360.field_0008->mpStarted = 0;
            break;
        case WM_STATECODE_CHILD_CONNECTED:
            if (native_data_main_020ec360.field_0008->endReq == 1)
                break;
            native_data_main_020ec360.field_0008->child_bitmap |= (0x1 << callback->aid);
            native_data_main_020ec360.field_0008->callback(0 , arg);
            if ((native_data_main_020ec360.field_0008->mpStarted == 0) && (!native_data_main_020ec360.field_000c->start_mp_busy)) {
                native_data_main_020ec360.field_000c->start_mp_busy = 1 ;
                errcode = native_fn_02012fdc(native_main_02016e08, (u16 *)native_data_main_020ec360.field_0008->recvBuf, native_data_main_020ec360.field_0008->recvBufSize, (u16 *)native_data_main_020ec360.field_0008->sendBuf, native_data_main_020ec360.field_0008->sendBufSize, (u16)(native_data_main_020ec360.field_0008->contSend ? 0 : 1), 0,
                                       0 , 0 , 1,
                                       1
                                       );
                native_fn_020189b0(WM_APIID_START_MP, errcode);
            } else {
                if (native_fn_02016d14()) {
                    native_data_main_020ec360.field_0008->callback(25 , ((void *)0) );
                }
            }
            break;
        case WM_STATECODE_DISCONNECTED:
            native_data_main_020ec360.field_0008->child_bitmap &= ~(0x1 << callback->aid);
            native_data_main_020ec360.field_0008->callback(1 , arg);
            break;
        case WM_STATECODE_DISCONNECTED_FROM_MYSELF:
            break;
        case WM_STATECODE_BEACON_SENT:
            if (native_data_main_020ec360.field_0008->endReq == 1)
                break;
            native_data_main_020ec360.field_0008->callback(28 , arg);
            break;
        default:
            native_data_main_020ec360.field_0008->callback(256 , arg);
            break;
        }
    }
    break;
    case WM_APIID_START_MP:
    {
        WMstartMPCallback * callback = (WMstartMPCallback *)arg;
        native_data_main_020ec360.field_000c->start_mp_busy = 0 ;
        switch (callback->state) {
        case WM_STATECODE_MP_START:
            native_data_main_020ec360.field_0008->mpStarted = 1;
            {
                if (native_data_main_020ec360.field_0008->endReq == 0) {
                    native_data_main_020ec360.field_0008->callback(25 , ((void *)0) );
                }
            }
            break;
        case WM_STATECODE_MPEND_IND:
            native_data_main_020ec360.field_0008->callback(3 , (void *)(callback->recvBuf));
            break;
        default:
            native_data_main_020ec360.field_0008->callback(256 , arg);
            break;
        }
        break;
    }
    break;
    case WM_APIID_SET_MP_DATA:
    {
        if (((MB_CommPWork *)native_data_main_020ec360.field_000c) ->useWvrFlag) {
            MbWaitForWvr(13000);
        }
        native_data_main_020ec360.field_0008->mpBusy = 0;
        if (buf->errcode == WM_ERRCODE_SUCCESS) {
            native_data_main_020ec360.field_0008->callback(2 , arg);
            if (native_data_main_020ec360.field_0008->endReq == 0) {
                native_data_main_020ec360.field_0008->callback(25 , ((void *)0) );
            }
        } else if (buf->errcode == WM_ERRCODE_SEND_QUEUE_FULL)   {
            native_data_main_020ec360.field_0008->callback(42 , arg);
        } else {
            native_data_main_020ec360.field_0008->callback(19 , arg);
            if (native_data_main_020ec360.field_0008->endReq == 0) {
                native_data_main_020ec360.field_0008->callback(25 , ((void *)0) );
            }
        }
    }
    break;
    case WM_APIID_RESET:
        if (!native_data_main_020ec360.field_000c->is_started_ex) {
            if (buf->errcode != WM_ERRCODE_SUCCESS) {
                native_data_main_020ec360.field_0008->endReq = 0;
                native_data_main_020ec360.field_0008->callback(256 , arg);
            } else {
                native_data_main_020ec360.field_0008->child_bitmap = 0;
                native_data_main_020ec360.field_0008->mpStarted = 0;
                errcode = native_fn_02012824(native_main_02016e08);
                native_fn_020189b0(WM_APIID_END, errcode);
            }
        } else {
            (void)native_fn_02011f58(WM_PORT_BT, ((void *)0) , ((void *)0) );
            (void)native_fn_02011f14(((void *)0) );
            if (buf->errcode != WM_ERRCODE_SUCCESS) {
                native_data_main_020ec360.field_0008->endReq = 0;
                native_data_main_020ec360.field_0008->callback(256 , arg);
            } else {
                errcode = native_fn_020141b0(native_main_02016e08, 0);
                native_fn_020189b0(WM_APIID_SET_BEACON_IND, errcode);
            }
        }
        break;
    case WM_APIID_END:
    {
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            native_data_main_020ec360.field_0008->endReq = 0;
            native_data_main_020ec360.field_0008->callback(256 , arg);
        } else {
            native_fn_02016dc4(arg);
        }
    }
    break;
    case WM_APIID_DISCONNECT:
    {
        WMDisconnectCallback * callback = (WMDisconnectCallback *)arg;
        if (buf->errcode != WM_ERRCODE_SUCCESS) {
            return;
        }
        native_data_main_020ec360.field_0008->child_bitmap &= ~(callback->disconnectedBitmap);
    }
    break;
    case WM_APIID_INDICATION:
    {
        WMindCallback * cb = (WMindCallback *)arg;
        switch (cb->state) {
        case WM_STATECODE_BEACON_RECV:
            native_data_main_020ec360.field_0008->callback(29 , arg);
            break;
        case WM_STATECODE_DISASSOCIATE:
            native_data_main_020ec360.field_0008->callback(31 , arg);
            break;
        case WM_STATECODE_REASSOCIATE:
            native_data_main_020ec360.field_0008->callback(32 , arg);
            break;
        case WM_STATECODE_AUTHENTICATE:
            native_data_main_020ec360.field_0008->callback(33 , arg);
            break;
        case WM_STATECODE_FIFO_ERROR:
            native_fn_02008430() ;
            break;
        case WM_STATECODE_INFORMATION:
            break;
        }
    }
    break;
    default:
        native_data_main_020ec360.field_0008->callback(256 , arg);
        break;
    }
}
