#include "context_00.h"
WMMpRecvData * native_main_020121ac (const WMMpRecvHeader * header, u16 aid)
{
    int i;
    WMErrCode result;
    WMMpRecvData * recvdata_p[15 ];
    WMArm9Buf * p = native_fn_020119c0();
    result = native_fn_020119d0();
    if (result != WM_ERRCODE_SUCCESS) {
        return ((void *)0) ;
    }
    if ((aid < 1) || (aid > 15 )) {
        ((void) 0) ;
        return ((void *)0) ;
    }
    native_fn_020072d0(&(p->status->child_bitmap), 2);
    if (0 == (p->status->child_bitmap & (0x0001 << aid))) {
        return ((void *)0) ;
    }
    if (header->count == 0) {
        return ((void *)0) ;
    }
    recvdata_p[0] = (WMMpRecvData *)(header->data);
    i = 0;
    do {
        if (recvdata_p[i]->aid == aid)
            return recvdata_p[i];
        ++i;
        recvdata_p[i] = (WMMpRecvData *)((u32)(recvdata_p[i - 1]) + header->length);
    } while (i < header->count);
    return ((void *)0) ;
}
