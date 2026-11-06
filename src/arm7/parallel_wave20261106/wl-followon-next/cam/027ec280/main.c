#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027ec280(void)
{
    LPWL_MAN pWlMan = (LPWL_MAN)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    LPCAM_ELEMENT pCAM = &pWlMan->Config.pCAM[1];
    LPDEAUTH_FRAME pTxDeAuthFrm;
    u32 pos, i;
    u32 cnt, state;
    cnt = pWlMan->CamMan.Count;
    for (i = 0, pos = 1; pos < pWlMan->Config.MaxStaNum; pos++, pCAM++) {
        if (pCAM->state != 0x00 ) {
            if ((pCAM->lifeTime != 0) && (pCAM->lifeTime != 0xFFFF) && (--pCAM->lifeTime == 0)) {
                if (pCAM->state >= 0x20 ) {
                    state = native_host_arm7_arm_027ebfec(pos);
                    native_host_arm7_main_027ebc50(pos, 0x20 );
                    native_host_arm7_arm_027f0d6c(pos);
                    if (pWlMan->Work.Mode == 1 ) {
                        if (state > 0x20 ) {
                            ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.NotSetTIM |= (1 << pos);
                            native_host_arm7_main_027ebd58(pos, 0);
                            CAM_SetAwake(pos);
                            pTxDeAuthFrm = native_host_arm7_arm_027f1ec8(pCAM->macAdrs, 1 , 0 );
                            if ((u32)pTxDeAuthFrm != (0) ) {
                                pTxDeAuthFrm->FirmHeader.FrameId = 0x0001 ;
                                native_host_arm7_arm_027f1088((LPTXFRM)pTxDeAuthFrm);
                                i++;
                                continue;
                            } else {
                                native_host_arm7_arm_027edbf0(pCAM->macAdrs, 1 );
                            }
                        }
                    } else {
                        if (pos == pWlMan->Work.APCamAdrs) {
                            pTxDeAuthFrm = native_host_arm7_arm_027f1ec8(pCAM->macAdrs, 1 , 0 );
                            if ((u32)pTxDeAuthFrm != (0) ) {
                                pTxDeAuthFrm->FirmHeader.FrameId = 0x0001 ;
                                native_host_arm7_arm_027f1088((LPTXFRM)pTxDeAuthFrm);
                                i++;
                                continue;
                            } else {
                                native_host_arm7_arm_037f9238(0x20 );
                                native_host_arm7_arm_027ea048();
                                native_host_arm7_arm_027edbf0(pCAM->macAdrs, 1 );
                            }
                        }
                    }
                }
                pCAM->state = 0x00 ;
                pWlMan->CamMan.Count--;
            }
            i++;
        }
        if (i >= cnt) {
            break;
        }
    }
}
