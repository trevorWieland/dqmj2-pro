#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027f1210(void)
{
    LPTXFRM_MAC pFrm = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Beacon.pMacFrm;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPBEACON_BODY pBody;
    u8 *pBuf;
    u8 *p;
    u32 i, vtsf;
    u16 *p16;
    p16 = (u16 *)&pFrm->MacHeader.Tx;
    *p16++ = 0;
    *p16++ = 0;
    *p16++ = 0;
    *p16++ = 0;
    *p16++ = native_host_arm7_arm_027ea584();
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x08 * 0x0010)) ;
    pFrm->Dot11Header.DurationID = 0;
    native_host_arm7_arm_027ea13c(pFrm->Dot11Header.Adrs1, (u16 *)native_host_arm7_data_027f74b0, pConfig->MacAdrs, pConfig->MacAdrs);
    pFrm->Dot11Header.SeqCtrl.Data = 0;
    pBody = (LPBEACON_BODY)pFrm->Body;
    pBody->TimeStamp[0] = 0;
    pBody->TimeStamp[1] = 0;
    pBody->BeaconInterval = pWork->BeaconPeriod;
    pBody->CapaInfo.Data = pWork->CapaInfo;
    pBuf = pBody->Buf;
    if (pConfig->BeaconType == 0 ) {
        pWork->Ofst.Beacon.SSID = (u16)((u32)pBuf - (u32)pFrm->Body);
        native_host_arm7_arm_027ead30(pBuf++, 0 );
        native_host_arm7_arm_027ead30(pBuf++, pWork->SSIDLength);
        for (i = 0; i < pWork->SSIDLength; i++) {
            native_host_arm7_arm_027ead30(pBuf++, native_host_arm7_arm_027ead5c(&pWork->SSID[i]));
        }
        native_host_arm7_arm_027ead30(&pBuf[-i - 1], i);
    } else {
        pWork->Ofst.Beacon.SSID = 0;
    }
    pBuf += native_host_arm7_arm_027f20dc(pBuf);
    native_host_arm7_arm_027ead30(pBuf++, 3 );
    native_host_arm7_arm_027ead30(pBuf++, 1);
    native_host_arm7_arm_027ead30(pBuf++, pWork->CurrChannel);
    pWork->Ofst.Beacon.TIM = (u16)((u32)pBuf - (u32)pBody);
    *(u16 *)((0x04808000) + 0x084) = pWork->Ofst.Beacon.TIM + 2;
    native_host_arm7_arm_027ead30(pBuf++, 5 );
    native_host_arm7_arm_027ead30(pBuf++, 3 + 2);
    native_host_arm7_arm_027ead30(pBuf++, 0);
    native_host_arm7_arm_027ead30(pBuf++, pWork->DTIMPeriod);
    native_host_arm7_arm_027ead30(pBuf++, 0);
    native_host_arm7_arm_027ead30(pBuf++, 0);
    native_host_arm7_arm_027ead30(pBuf++, 0);
    pWork->Ofst.Beacon.GameInfo = (u16)((u32)pBuf - (u32)pBody);
    pWork->GameInfoAlign = pWork->Ofst.Beacon.GameInfo & 1;
    native_host_arm7_arm_027ead30(pBuf++, 221 );
    native_host_arm7_arm_027ead30(pBuf++, 3 + 1 + 4 + pWork->GameInfoLength);
    native_host_arm7_arm_027ead30(pBuf++, 0x00 );
    native_host_arm7_arm_027ead30(pBuf++, 0x09 );
    native_host_arm7_arm_027ead30(pBuf++, 0xBF );
    native_host_arm7_arm_027ead30(pBuf++, 0x00 );
    if (pWork->PowerMgtMode == 1 ) {
        native_host_arm7_arm_027ead30(pBuf++, pConfig->ActiveZone);
        native_host_arm7_arm_027ead30(pBuf++, (pConfig->ActiveZone >> 8));
    } else {
        native_host_arm7_arm_027ead30(pBuf++, 0xFF);
        native_host_arm7_arm_027ead30(pBuf++, 0xFF);
    }
    vtsf = *(u16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
    native_host_arm7_arm_027ead30(pBuf++, vtsf & 0x00FF);
    native_host_arm7_arm_027ead30(pBuf++, vtsf >> 8);
    p = (u8 *)pWork->GameInfoAdrs;
    for (i = 0; i < pWork->GameInfoLength; i++) {
        native_host_arm7_arm_027ead30(pBuf++, native_host_arm7_arm_027ead5c(p));
        p++;
    }
    if (pWork->GameInfoAlign) {
        p = (u8 *)((u32)pWork->GameInfoAdrs + pWork->GameInfoLength - 1);
        for (i = 0; i < pWork->GameInfoLength; i++, p--) {
            native_host_arm7_arm_027ead30(p + 1, native_host_arm7_arm_027ead5c(p));
        }
    }
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000004 ) {
        u16 *pId = (u16 *)(((u32)pBuf + 3) & 0xFFFFFFFC);
        pId[0] = 0xB6B8 ;
        pId[1] = 0x1D46 ;
    }
    pWork->bUpdateGameInfo = 0 ;
    pFrm->MacHeader.Tx.MPDU = 24 + (u32)pBuf - (u32)pBody + 4;
}

#include "context003.h"
