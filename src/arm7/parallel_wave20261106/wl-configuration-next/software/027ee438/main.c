#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027ee438(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    WlParamSetLifeTimeReq *pReq = (WlParamSetLifeTimeReq *)pReqt;
    LPCAM_ELEMENT pCAM = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.pCAM;
    u32 i;
    pCfmt->header.length = 1;
    if ((pReq->tableNumber >= ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MaxStaNum) && (pReq->tableNumber != 0xFFFF)) {
        return 0x05 ;
    }
    if ((pReq->frameLifeTime > 63 ) && (pReq->frameLifeTime != 0xFFFF)) {
        return 0x05 ;
    }
    if (pReq->tableNumber == 0xFFFF) {
        for (i = 1; i < ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MaxStaNum; i++) {
            pCAM[i].maxLifeTime = pReq->camLifeTime;
            if (pCAM[i].lifeTime != 0) {
                pCAM[i].lifeTime = pReq->camLifeTime;
            }
        }
    } else if (pReq->tableNumber != 0) {
        pCAM[pReq->tableNumber].maxLifeTime = pReq->camLifeTime;
        if (pCAM[pReq->tableNumber].lifeTime != 0) {
            pCAM[pReq->tableNumber].lifeTime = pReq->camLifeTime;
        }
    }
    if (pReq->frameLifeTime != 0) {
        native_host_arm7_arm_027e9e3c(pReq->frameLifeTime);
    }
    return 0x00 ;
}
