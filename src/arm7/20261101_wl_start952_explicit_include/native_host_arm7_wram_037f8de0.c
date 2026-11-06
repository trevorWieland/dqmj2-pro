#include "../20261101_wl_counter504/wl_complete_types.h"
extern u64 native_host_arm7_wram_03806bf0(u64 numerator,u64 denominator);
void WStop(void);
void RND_init(u32 a, u32 b);
void InitCAM(void);
void InitApList(void);
void InitTxCtrl(void);
void InitRxCtrl(void);
void WSetStaState(u32 state);
void StartBeaconFrame(void);
void WDisableTmpttPowerSave(void);
u16 WSetPowerState(u32 state);
void WaitLoop_Rxpe(void);

void native_host_arm7_wram_037f8de0(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    u32 bp;
    u16 *ptsf;
    u64 lltsf;
    WStop();
    RND_init((u32)(*(vu16 *)(0x04808000 + 0x044) + (*(vu16 *)(0x04808000 + 0x044) << 8)), *(vu16 *)(0x04808000 + 0x044) );
    pWork->CapaInfo = (0x01 << 0) ;
    if (pConfig->PreambleType == 1 ) {
        pWork->CapaInfo |= (0x01 << 5) ;
    }
    if (pConfig->WepMode != 0 ) {
        pWork->CapaInfo |= (0x01 << 4) ;
    }
    pWork->bSynchro = 0;
    *(vu16 *)((0x04808000) + 0x032) = (0x8000) ;
    *(vu16 *)((0x04808000) + 0x134) = 0xFFFF;
    *(vu16 *)((0x04808000) + 0x02A) = 0;
    *(vu16 *)((0x04808000) + 0x028) = 0;
    *(vu16 *)((0x04808000) + 0x038) = (0x0001 << 3) | (0x0001 << 2) | (0x0001 << 1) | (0x0001 << 0) ;
    InitCAM();
    InitApList();
    InitTxCtrl();
    InitRxCtrl();
    *(u16 *)((0x04808000) + 0x030) = 0x8000;
    *(vu16 *)((0x04808000) + 0x010) = 0xFFFF;
    *(vu16 *)((0x04808000) + 0x1AE) = 0x1FFF;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000008 ) {
        *(vu16 *)((0x04808000) + 0x1AA) = (0x0001 << 10) ;
    } else {
        *(vu16 *)((0x04808000) + 0x1AA) = 0;
    }
    *(vu16 *)((0x04808000) + 0x008) = 0;
    *(vu16 *)((0x04808000) + 0x00A) = 0;
    switch (pWork->Mode) {
    case 0 :
        *(vu16 *)((0x04808000) + 0x012) = (0x0001 << 5) | (0x0003 << 4) | (0x0001 << 3) | (0x0001 << 1) | (0x0001 << 2) | (0x0001 << 0) ;
        *(vu16 *)((0x04808000) + 0x0D0) = 0xFFFF;
        *(vu16 *)((0x04808000) + 0x0E0) = ((0x0001 << 3)) ;
        *(vu16 *)((0x04808000) + 0x008) = 0;
        *(vu16 *)((0x04808000) + 0x00A) = 0;
        *(vu16 *)((0x04808000) + 0x0E8) = 0;
        *(vu16 *)((0x04808000) + 0x004) = (0x0001 << 0) ;
        break;
    case 1 :
        *(vu16 *)((0x04808000) + 0x012) = (0x0001 << 14) | (0x0001 << 13) | (0x0001 << 5) | (0x0003 << 4) | (0x0001 << 3) | (0x0001 << 1) | (0x0001 << 2) | (0x0001 << 0) | (0x0001 << 12) | 0;
        *(vu16 *)((0x04808000) + 0x1AE) = 0x1FFF;
        *(vu16 *)((0x04808000) + 0x0D0) = (0x0001 << 0) | (0x0001 << 9) | (0x0001 << 8) ;
        *(vu16 *)((0x04808000) + 0x0E0) = ((0x0001 << 3) | (0x0001 << 2) | (0x0001 << 0)) ;
        *(vu16 *)((0x04808000) + 0x008) = (0x0001 << 15) | (0x0001 << 14) | (0x0001 << 13) ;
        *(vu16 *)((0x04808000) + 0x004) = (0x0001 << 0) ;
        ptsf = (u16 *)&lltsf;
        ptsf[0] = *(vu16 *)((0x04808000) + 0x0F8) ;
        ptsf[1] = *(vu16 *)((0x04808000) + 0x0FA) ;
        ptsf[2] = *(vu16 *)((0x04808000) + 0x0FC) ;
        ptsf[3] = *(vu16 *)((0x04808000) + 0x0FE) ;
        bp = (u32)pWork->BeaconPeriod * 1024;
        lltsf = native_host_arm7_wram_03806bf0(lltsf,(u64)bp);
        lltsf++;
        lltsf *= bp;
        *(vu16 *)((0x04808000) + 0x0F6) = ptsf[3];
        *(vu16 *)((0x04808000) + 0x0F4) = ptsf[2];
        *(vu16 *)((0x04808000) + 0x0F2) = ptsf[1];
        *(vu16 *)((0x04808000) + 0x0F0) = (u16)(ptsf[0] | 0x0001);
        *(vu16 *)((0x04808000) + 0x0E8) = 1;
        *(vu16 *)((0x04808000) + 0x0EA) = 1;
        WSetStaState(0x40 );
        StartBeaconFrame();
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 1) ;
        break;
    case 2 :
        *(vu16 *)((0x04808000) + 0x012) = (0x0001 << 15) | (0x0001 << 14) | (0x0001 << 13) | (0x0001 << 5) | (0x0003 << 4) | (0x0001 << 3) | (0x0001 << 1) | (0x0001 << 2) | (0x0001 << 0) | (0x0001 << 7) | 0;
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000020 ) {
            *(vu16 *)((0x04808000) + 0x012) |= (0x0001 << 6) ;
            *(vu16 *)((0x04808000) + 0x1AA) |= ((0x0001 << 5) | (0x0001 << 6) | (0x0001 << 3) );
        }
        if (pWork->BSSID[0] & 0x001) {
            *(vu16 *)((0x04808000) + 0x0D0) = (0x0001 << 0) | (0x0001 << 8) | (0x0001 << 7) | (0x0001 << 10) ;
        } else {
            *(vu16 *)((0x04808000) + 0x0D0) = (0x0001 << 0) | (0x0001 << 8) | (0x0001 << 7) ;
        }
        *(vu16 *)((0x04808000) + 0x0E0) = ((0x0001 << 3) | (0x0001 << 1) | (0x0001 << 0)) ;
        *(vu16 *)((0x04808000) + 0x004) = (0x0001 << 0) ;
        *(vu16 *)((0x04808000) + 0x0E8) = 1;
        *(vu16 *)((0x04808000) + 0x0EA) = 1;
        WSetStaState(0x20 );
        break;
    case 3 :
        *(vu16 *)((0x04808000) + 0x010) = 0xFFFF;
        *(vu16 *)((0x04808000) + 0x012) = (0x0001 << 15) | (0x0001 << 14) | (0x0001 << 5) | (0x0003 << 4) | (0x0001 << 3) | (0x0001 << 1) | (0x0001 << 2) | (0x0001 << 0) | 0;
        if (pWork->BSSID[0] & 0x001) {
            *(vu16 *)((0x04808000) + 0x0D0) = (0x0001 << 0) | (0x0001 << 10) ;
        } else {
            *(vu16 *)((0x04808000) + 0x0D0) = (0x0001 << 0) ;
        }
        *(vu16 *)((0x04808000) + 0x0E0) = ((0x0001 << 3) | (0x0001 << 1) | (0x0001 << 0)) ;
        *(vu16 *)((0x04808000) + 0x004) = (0x0001 << 0) ;
        *(vu16 *)((0x04808000) + 0x0E8) = 1;
        *(vu16 *)((0x04808000) + 0x0EA) = 1;
        *(vu16 *)((0x04808000) + 0x048) = 0;
        WSetStaState(0x20 );
        break;
    case (3 + 1) :
        *(vu16 *)((0x04808000) + 0x012) = 0x0000;
        *(vu16 *)((0x04808000) + 0x1AE) = 0x0000;
        *(vu16 *)((0x04808000) + 0x004) = (0x0001 << 0) ;
        WSetStaState(0x20 );
        break;
    }
    *(vu16 *)((0x04808000) + 0x048) = 0;
    WDisableTmpttPowerSave();
    *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 1) ;
    if (pWork->PowerMgtMode == 1 ) {
        WSetPowerState((0x0001 << 1) );
    }
    WaitLoop_Rxpe();
}
