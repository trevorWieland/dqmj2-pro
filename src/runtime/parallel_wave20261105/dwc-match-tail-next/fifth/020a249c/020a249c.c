#include "context.h"
void native_main_020a249c (u8 aid, u16 type)
{
    u8 i;
    u8 senddata[4];
    DWC_Printf(DWC_REPORTFLAG_MATCH_GT2, "Sent SYN %d packet to aid %d.\n",
               type - DWC_SEND_TYPE_MATCH_SYN, aid);
    switch (type) {
    case DWC_SEND_TYPE_MATCH_SYN:
        if (aid == native_fn_020a3d70()->aidList[native_fn_020a3d70()->gt2NumConnection]) {
            senddata[0] = 1;
        } else {
            senddata[0] = 0;
        }
        for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
            if (aid == native_fn_020a3d70()->aidList[i]) {
                senddata[1] = i;
                senddata[2] = aid;
                break;
            }
        }
        break;
    case DWC_SEND_TYPE_MATCH_SYN_ACK:
        senddata[0] = (u8)(native_fn_020a3d70()->baseLatency & 0xff);
        senddata[1] = (u8)((native_fn_020a3d70()->baseLatency >> 8) & 0xff);
        break;
    }
    native_fn_020a3f84(type, aid, senddata, DWC_MATCH_SYN_DATA_BODY_SIZE);
    native_fn_020a3d70()->lastSynSent = native_fn_02007a9c();
}
