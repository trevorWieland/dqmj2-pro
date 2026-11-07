#include "context000.h"

#include "context001.h"

#include "context002.h"

u32 native_host_arm7_main_027e89ec(WlInit *pInit)
{
    u32 adrs = pInit->workingMemAdrs;
    u16 sts;
    *(u32 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34) ) = adrs;
    MI_CpuClearFast((void *)adrs, sizeof(WL_MAN));
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->lockID = native_host_arm7_arm_037fbbfc();
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->DmaChannel = pInit->dmaChannel;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->DmaMaxCount = pInit->dmaMaxSize / 2;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->DmaMaxCount == 0) {
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->DmaMaxCount = 0xFFFFFFFF;
    }
    native_host_arm7_arm_027e8c78((LPHEAP_INFO)&pInit->heapType);
    native_host_arm7_arm_027f4ecc();
    (*( REGType16v *) (0x04000000 + 0x304)) |= 0x0002;
    *(vu16 *)(0x04000000 + 0x206) = 0x0030;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlDbgLevel = 0x0003;
    sts = 0;
    native_host_arm7_arm_027f4e1c((u32)(&((LPFLASH_TABLE)0x002a)->enableChannel) , 2, (u8 *)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->EnableChannel);
    native_host_arm7_arm_027f4e1c((u32)(&((LPFLASH_TABLE)0x002a)->wlOperation) , 2, (u8 *)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation);
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pRecvMsgQueue = pInit->sendMsgQueuep;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pSendMsgQueue = pInit->recvMsgQueuep;
    native_host_arm7_arm_027e8de8((LPCAM_ELEMENT)pInit->camAdrs, pInit->camSize / sizeof(CAM_ELEMENT));
    native_host_arm7_arm_027e8bd0();
    native_host_arm7_arm_027ec6f0();
    native_host_arm7_arm_027ee0bc();
    native_host_arm7_arm_027ec480();
    native_host_arm7_arm_027ea954();
    {
        u32 crc;
        if (native_host_arm7_arm_027f4d38(&crc) != 0) {
            ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult |= 0x0080 ;
            goto exit_init;
        }
    }
    native_host_arm7_arm_027ea6bc();
    native_host_arm7_arm_027eb22c();
    native_host_arm7_main_027e9d88();
    native_host_arm7_arm_027ea72c();
    if (sts == 0) {
        native_host_arm7_arm_027ea7cc();
    }
    native_host_arm7_arm_027eb3d0();
    ;
    native_host_arm7_arm_027eb55c();
    if (sts == 0) {
        native_host_arm7_arm_027ea764();
    }
    native_host_arm7_main_027e97bc();
    native_host_arm7_arm_027e9d00();
exit_init:
    native_host_arm7_arm_037fc054(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan.Thread, native_host_arm7_arm_037f84e0, 0 , pInit->stack, pInit->stacksize, pInit->priority);
    native_host_arm7_arm_037fc36c(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan.Thread);
    native_host_arm7_arm_027eb8c8();
    return ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult;
}
