#include "context_00.h"
int native_main_02017f64 (void * work, const MBUserInfo * user, u32 ggid, u32 tgid, u32 dma)
{
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    if (native_data_main_020ec360.field_000c && native_data_main_020ec360.field_000c->isMbInitialized) {
        return MB_ERRCODE_INVALID_STATE;
    } else {
        MBiParam * const p_parm = (MBiParam *) ((((u32)work) + 0x1F) & ~0x1F);
        MB_CommCommonWork * const p_com = (MB_CommCommonWork *) ((((u32)p_parm) + sizeof(*p_parm) + 0x1F) & ~0x1F);
        OSIntrMode enabled;
        if (tgid == 0x10000 ) {
            tgid = native_fn_020125bc();
        }
        enabled = native_fn_02007ff4();
        native_data_main_020dce94.field_0006 = 0xFFFF ;
        native_data_main_020dce94.field_0000 = 5 ;
        native_data_main_020dce94.field_0002 = 40 ;
        native_data_main_020dce94.field_0004 = 40 ;
        native_data_main_020dce94.field_000c = 1 ;
        native_data_main_020ec360.field_0000 = (u16)dma;
        native_data_main_020ec360.field_0008 = p_parm;
        native_data_main_020ec360.field_000c = p_com;
        MI_CpuClear32(p_parm, sizeof(*p_parm));
        MI_CpuClear16(p_com, sizeof(*p_com));
        {
            int i;
            u16 * c;
            c = (u16 *)p_parm->uname;
            for (i = 0; i < user->nameLength; ++i) {
                *c++ = user->name[i];
            }
            c = (u16 *)p_parm->gname;
            for (i = 0; i < 16 ; ++i) {
                if (*native_data_main_020dce94.field_0008 == 0) {
                    break;
                }
                *c++ = *native_data_main_020dce94.field_0008++;
            }
            native_fn_02008e0c(user, &p_com->user, sizeof(MBUserInfo));
            if (user->nameLength < 10 ) {
                p_com->user.name[user->nameLength] = 0;
            }
        }
        {
            p_parm->p_sendlen = (256) ;
            p_parm->p_recvlen = (8) ;
            p_parm->sendBufSize = 0;
            p_parm->recvBufSize = 0;
            p_parm->contSend = 1;
            p_parm->recvBuf = (WMmpRecvBuf *)p_com->recvbuf;
            {
                WMParentParam * const p_parent = &p_parm->parentParam;
                p_parent->entryFlag = 0;
                p_parent->multiBootFlag = 0;
                p_parent->CS_Flag = 1;
                p_parent->KS_Flag = 0;
                p_parent->ggid = ggid;
                p_parent->tgid = (u16)tgid;
                p_parent->beaconPeriod = (u16)((200) + native_fn_02017efc());
                p_parent->maxEntry = 15;
            }
        }
        p_parm->mpBusy = 0;
        p_parm->mbIsStarted = 0;
        p_com->isMbInitialized = 1;
        p_com->start_mp_busy = 0 ;
        (void)native_fn_02008008(enabled);
    }
    return MB_ERRCODE_SUCCESS;
}
