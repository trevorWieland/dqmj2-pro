#include "context_00.h"
#include "context_01.h"
void native_main_02011ac8 (PXIFifoTag tag, u32 fifo_buf_adr, BOOL err)
{
    WMCallback * callback_p = (WMCallback *)fifo_buf_adr;
    WMArm9Buf * w9b = native_data_main_020e5d80.field_0004;
    if (err)
        return;
    native_fn_020072d0(w9b->fifo7to9, 256 );
    if (!w9b->scanOnlyFlag) {
        native_fn_020072d0(w9b->status, 2048 );
    }
    if ((u32)callback_p != (u32)(w9b->fifo7to9)) {
        native_fn_020072d0(callback_p, 256 );
    }
    if (callback_p->apiid >= (WM_APIID_ASYNC_KIND_MAX - 2) ) {
        if (callback_p->apiid == WM_APIID_INDICATION) {
            if (callback_p->errcode == WM_ERRCODE_FLASH_ERROR) {
                native_fn_02008430();
            }
            if (w9b->indCallback != ((void *)0) ) {
                w9b->indCallback((void *)callback_p);
            }
        } else if (callback_p->apiid == WM_APIID_PORT_RECV)   {
            WMPortRecvCallback * received_port_callback = (WMPortRecvCallback *)callback_p;
            ((void) 0) ;
            if (w9b->portCallbackTable[received_port_callback->port] != ((void *)0) ) {
                received_port_callback->arg = w9b->portCallbackArgument[received_port_callback->port];
                received_port_callback->connectedAidBitmap = (u16)w9b->connectedAidBitmap;
                native_fn_020072d0(received_port_callback->recvBuf, w9b->status->mp_recvBufSize);
                (w9b->portCallbackTable[received_port_callback->port])((void *)received_port_callback);
            }
        } else if (callback_p->apiid == WM_APIID_PORT_SEND)   {
            WMPortSendCallback * sent_port_callback = (WMPortSendCallback *)callback_p;
            callback_p->apiid = WM_APIID_SET_MP_DATA;
            if (sent_port_callback->callback != ((void *)0) ) {
                (sent_port_callback->callback)((void *)sent_port_callback);
            }
        } else {
            ((void)0) ;
        }
    } else {
        if (callback_p->apiid == WM_APIID_START_MP) {
            WMStartMPCallback * cb_StartMP = (WMStartMPCallback *)callback_p;
            if (cb_StartMP->state == WM_STATECODE_MPEND_IND
                || cb_StartMP->state == WM_STATECODE_MP_IND) {
                if (cb_StartMP->errcode == WM_ERRCODE_SUCCESS) {
                    native_fn_020072d0(cb_StartMP->recvBuf, w9b->status->mp_recvBufSize);
                }
            }
        }
        if (callback_p->apiid == WM_APIID_END) {
            if (callback_p->errcode == WM_ERRCODE_SUCCESS) {
                WMCallbackFunc cb = w9b->CallbackTable[callback_p->apiid];
                (void)native_fn_020117c4();
                if (cb != ((void *)0) ) {
                    cb((void *)callback_p);
                }
                ((void) 0) ;
                return;
            }
        }
        if (((void *)0) != w9b->CallbackTable[callback_p->apiid]) {
            (w9b->CallbackTable[callback_p->apiid])((void *)callback_p);
            if (!native_data_main_020e5d80.field_0000) {
                return;
            }
        }
        if (callback_p->apiid == WM_APIID_START_PARENT
            || callback_p->apiid == WM_APIID_START_CONNECT) {
            u16 state, aid, myAid, reason;
            u8 * macAddress;
            u8 * ssid;
            u16 parentSize, childSize;
            if (callback_p->apiid == WM_APIID_START_PARENT) {
                WMStartParentCallback * cb = (WMStartParentCallback *)callback_p;
                state = cb->state;
                aid = cb->aid;
                myAid = 0;
                macAddress = cb->macAddress;
                ssid = cb->ssid;
                reason = cb->reason;
                parentSize = cb->parentSize;
                childSize = cb->childSize;
            } else if (callback_p->apiid == WM_APIID_START_CONNECT)   {
                WMStartConnectCallback * cb = (WMStartConnectCallback *)callback_p;
                state = cb->state;
                aid = 0;
                myAid = cb->aid;
                macAddress = cb->macAddress;
                ssid = ((void *)0) ;
                reason = cb->reason;
                parentSize = cb->parentSize;
                childSize = cb->childSize;
            }
            if (state == WM_STATECODE_CONNECTED ||
                state == WM_STATECODE_DISCONNECTED
                || state == WM_STATECODE_DISCONNECTED_FROM_MYSELF) {
                u16 iPort;
                if (state == WM_STATECODE_CONNECTED) {
                    ((void) 0)                                       ;
                    w9b->connectedAidBitmap |= (1 << aid);
                } else {
                    ((void) 0)                                       ;
                    w9b->connectedAidBitmap &= ~(1 << aid);
                }
                w9b->myAid = myAid;
                MI_CpuClear8(&native_data_main_020e5d80.field_0050, sizeof(WMPortRecvCallback));
                native_data_main_020e5d80.field_0050.apiid = WM_APIID_PORT_RECV;
                native_data_main_020e5d80.field_0050.errcode = WM_ERRCODE_SUCCESS;
                native_data_main_020e5d80.field_0050.state = state;
                native_data_main_020e5d80.field_0050.recvBuf = ((void *)0) ;
                native_data_main_020e5d80.field_0050.data = ((void *)0) ;
                native_data_main_020e5d80.field_0050.length = 0;
                native_data_main_020e5d80.field_0050.aid = aid;
                native_data_main_020e5d80.field_0050.myAid = myAid;
                native_data_main_020e5d80.field_0050.connectedAidBitmap = (u16)w9b->connectedAidBitmap;
                native_data_main_020e5d80.field_0050.seqNo = 0xffff;
                native_data_main_020e5d80.field_0050.reason = reason;
                native_fn_02008e0c(macAddress, native_data_main_020e5d80.field_0050.macAddress, 6 );
                if (ssid != ((void *)0) ) {
                    MI_CpuCopy16(ssid, native_data_main_020e5d80.field_0050.ssid, 24 );
                } else {
                    MI_CpuClear16(native_data_main_020e5d80.field_0050.ssid, 24 );
                }
                native_data_main_020e5d80.field_0050.maxSendDataSize = (myAid == 0) ? parentSize : childSize;
                native_data_main_020e5d80.field_0050.maxRecvDataSize = (myAid == 0) ? childSize : parentSize;
                for (iPort = 0; iPort < 16 ; iPort++) {
                    native_data_main_020e5d80.field_0050.port = iPort;
                    if (w9b->portCallbackTable[iPort] != ((void *)0) ) {
                        native_data_main_020e5d80.field_0050.arg = w9b->portCallbackArgument[iPort];
                        (w9b->portCallbackTable[iPort])((void *)&native_data_main_020e5d80.field_0050);
                    }
                }
            }
        }
    }
    native_fn_020072d0(w9b->fifo7to9, 256 );
    native_fn_02011e74();
    if ((u32)callback_p != (u32)(w9b->fifo7to9)) {
        callback_p->apiid |= 0x8000 ;
        native_fn_020072ec(callback_p, 256 );
    }
    ((void) 0) ;
    return;
}
