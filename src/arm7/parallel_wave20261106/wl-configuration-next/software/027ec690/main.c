#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ec690(void)
{
    u16 *pMsg = (u16 *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->HeapMan.ToWM).Head) ;
    while ((u32)pMsg != (u32)(-1) ) {
        if (native_host_arm7_arm_037fc6d4(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pSendMsgQueue, pMsg, 0 )) {
            native_host_arm7_arm_037f87ac(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.ToWM, (LPHEAPBUF_HEADER)pMsg);
            pMsg = (u16 *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->HeapMan.ToWM).Head) ;
        } else {
            break;
        }
    }
}
