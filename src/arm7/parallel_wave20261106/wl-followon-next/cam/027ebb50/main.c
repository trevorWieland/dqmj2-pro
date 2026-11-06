#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ebb50(LPTXFRM pFrm)
{
    LPCAM_ELEMENT pCAM;
    u32 x, cam_adrs;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    pCAM = CAM_GetTbl(cam_adrs);
    x = native_host_arm7_arm_037fb928((1UL << 24) );
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.Mode == 1 ) {
        if (pCAM->frameCount == 0) {
            native_host_arm7_arm_027ec118(cam_adrs);
        }
    }
    pCAM->frameCount++;
    native_host_arm7_arm_037fb8f0(x);
    if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.NotSetTIM & (1 << cam_adrs)) == 0) {
        pCAM->lifeTime = pCAM->maxLifeTime;
    }
}

#include "context002.h"
