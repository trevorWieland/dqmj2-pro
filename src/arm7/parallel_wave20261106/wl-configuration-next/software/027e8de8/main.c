#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e8de8(LPCAM_ELEMENT pCam, u32 staNum)
{
    void *pGameInfo = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.GameInfoAdrs;
    MI_CpuClear16((void *)(u32)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->Config, sizeof(CONFIG_PARAM)) ;
    MI_CpuClear16((void *)(u32)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->Work, sizeof(WORK_PARAM)) ;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.pCAM = pCam;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.CamMaxStaNum = (u16)staNum;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MaxStaNum = (u16)staNum;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.GameInfoAdrs = pGameInfo;
}
