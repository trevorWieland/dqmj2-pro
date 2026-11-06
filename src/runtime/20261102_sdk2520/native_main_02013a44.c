#include "native_main_02013a44_types.h"

void native_main_02013a44 (void * callback)
{
    WMArm9Buf * p = native_fn_020119c0();
    WMPortSendCallback * cb_Port = (WMPortSendCallback *)callback;
    WMDataSharingInfo * dsInfo;
    u16 aid;
    dsInfo = (WMDataSharingInfo *)(p->portCallbackArgument[cb_Port->port]);
    if ((p->portCallbackTable[cb_Port->port] != native_data_main_02013b1c
         && p->portCallbackTable[cb_Port->port] != native_data_main_02013c48)
        || dsInfo == ((void *)0) || dsInfo != (WMDataSharingInfo *)(cb_Port->arg)) {
        ((void) 0) ;
        return;
    }
    aid = native_fn_02011eb4();
    if (cb_Port->errcode == WM_ERRCODE_SUCCESS) {
        if (aid == 0) {
            ((void) 0)
                                 ;
            dsInfo->seqNum[dsInfo->sendIndex] = (u16)(cb_Port->seqNo >> 1);
            dsInfo->sendIndex = WmDataSharingGetNextIndex(dsInfo->sendIndex);
        } else {
            ((void) 0)
                                 ;
        }
    } else {
        if (cb_Port->errcode == WM_ERRCODE_SEND_QUEUE_FULL) {
            if (aid != 0) {
                dsInfo->sendIndex = WmDataSharingGetPrevIndex(dsInfo->sendIndex);
            }
            dsInfo->state = WM_DS_STATE_RETRY_SEND;
            ((void) 0) ;
        } else {
            ((void) 0)
                       ;
            dsInfo->state = WM_DS_STATE_ERROR;
        }
    }
}
void native_data_main_02013b1c (void * callback);
void native_data_main_02013c48 (void * callback);
