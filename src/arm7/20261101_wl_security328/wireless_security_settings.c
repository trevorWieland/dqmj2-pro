#include "beacon_types.h"
extern unsigned int native_arm7_main_027e9bd8(void);


u16 native_host_arm7_main_027e8ff0(u16 mode)
{
    LPBEACON_BODY pBody;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    if (mode > 3 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.WepMode = mode;
    if (mode == 0 ) {
        pWork->CapaInfo &= ~(0x01 << 4) ;
        pWork->FrameCtrl &= ~0x4000 ;
    } else {
        pWork->CapaInfo |= (0x01 << 4) ;
        pWork->FrameCtrl |= 0x4000 ;
    }
    if ((pWork->STA == 0x40 ) && (mode == 1 )) {
        pBody = (LPBEACON_BODY)((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm->Body;
        pBody->CapaInfo.Data = pWork->CapaInfo;
    }
    if (mode == 0) {
        mode = 1;
    }
    *(vu16 *)((0x04808000) + 0x006) = (u16)((*(vu16 *)((0x04808000) + 0x006) & (u16)~ (0x0007 << 3)) | ((u16) mode * (0x0001 << 3))) ;
    return 0;
}


u16 native_host_arm7_main_027e929c(u16 type)
{
    LPBEACON_BODY pBody;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    if (type > 1 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.PreambleType = type;
    if (type == 0 ) {
        pWork->CapaInfo &= ~(0x01 << 5) ;
    } else {
        pWork->CapaInfo |= (0x01 << 5) ;
    }
    if ((pWork->STA == 0x40 ) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode == 1 )) {
        pBody = (LPBEACON_BODY)((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm->Body;
        pBody->CapaInfo.Data = pWork->CapaInfo;
    }
    if (type == 0 ) {
        *(vu16 *)((0x04808000) + 0x0BC) &= ~((0x0001 << 1) | (0x0001 << 2) );
    } else {
        *(vu16 *)((0x04808000) + 0x0BC) |= ((0x0001 << 1) | (0x0001 << 2) );
    }
    native_arm7_main_027e9bd8();
    return 0;
}
