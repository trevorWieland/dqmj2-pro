#include "context000.h"

#include "context001.h"

BOOL native_host_arm7_main_027e8110(u16 *pWlCommand, u16 *pWlResult)
{
    WMStatus *status = WMSP_GetStatusStructure();
    WlCmdCfm *pConfirm;
    u32 wlBuf[128];
    u16 enableChannel = 0x0000;
    {
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e28c8((u16 *)wlBuf);
        if (pConfirm->resultCode != 0x00 ) {
            *pWlCommand = (0x0300 | 0x04) ;
            *pWlResult = pConfirm->resultCode;
            return 0 ;
        }
    }
    {
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2898((u16 *)wlBuf);
        if (pConfirm->resultCode != 0x00 ) {
            *pWlCommand = (0x0300 | 0x02) ;
            *pWlResult = pConfirm->resultCode;
            return 0 ;
        }
    }
    WmspStabilizeBeacon();
    {
        WlParamGetEnableChannelCfm *pECConfirm;
        pECConfirm = (WlParamGetEnableChannelCfm *)native_host_arm7_arm_027e2854((u16 *)wlBuf);
        if (pECConfirm->resultCode != 0x00 ) {
            *pWlCommand = (0x0200 | 0x83) ;
            *pWlResult = pECConfirm->resultCode;
            return 0 ;
        }
        enableChannel = pECConfirm->enableChannel;
    }
    status->enableChannel = enableChannel;
    status->allowedChannel = native_host_arm7_arm_03807444((u16)(enableChannel >> 1));
    {
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e25e0((u16 *)wlBuf, 0xffff,
            40 ,
            5
        );
        status->mp_lifeTimeTick = ((OSTick)(((33514000 / 1000) * (u64)(40 * 100)) / 64)) ;
    }
    status->rate = 2 ;
    status->preamble = 1 ;
    {
        WlDevGetVerInfoCfm *pVConfirm;
        pVConfirm = (WlDevGetVerInfoCfm *)native_host_arm7_arm_027e28f4((u16 *)wlBuf);
        if (pVConfirm->resultCode != 0x00 ) {
            *pWlCommand = (0x0300 | 0x06) ;
            *pWlResult = pVConfirm->resultCode;
            return 0 ;
        }
        MI_CpuCopy16(pVConfirm->wlVersion, status->wlVersion, 8 );
        status->macVersion = pVConfirm->macVersion;
        status->bbpVersion[0] = pVConfirm->bbpVersion[0];
        status->bbpVersion[1] = pVConfirm->bbpVersion[1];
        status->rfVersion = pVConfirm->rfVersion;
    }
    {
        WlParamGetMacAdrsCfm *pMConfirm;
        pMConfirm = (WlParamGetMacAdrsCfm *)native_host_arm7_arm_027e283c((u16 *)wlBuf);
        if (pMConfirm->resultCode != 0x00 ) {
            *pWlCommand = (0x0200 | 0x81) ;
            *pWlResult = pMConfirm->resultCode;
            return 0 ;
        }
        native_host_arm7_arm_037fe12c(pMConfirm->staMacAdrs, status->MacAddress, 6 );
    }
    {
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e26a4((u16 *)wlBuf, 1);
        if (pConfirm->resultCode != 0x00 ) {
            *pWlCommand = (0x0200 | 0x15) ;
            *pWlResult = pConfirm->resultCode;
            return 0 ;
        }
    }
    return 1 ;
}

#include "context002.h"
