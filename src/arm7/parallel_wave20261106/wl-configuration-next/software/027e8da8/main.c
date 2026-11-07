#include "context000.h"

void native_host_arm7_main_027e8da8(LPHEAPBUF_MAN pHeapBufMan)
{
    u32 *pNext;
    u32 *pBuf = (u32 *)((u32)(*(LPHEAPBUF_MAN)pHeapBufMan).Head) ;
    if (pHeapBufMan->Count != 0) {
        while ((u32)pBuf != (u32)(-1) ) {
            pNext = (u32 *)GetHeapBufNextAdrs(pBuf);
            native_host_arm7_arm_037f8908(pHeapBufMan, pBuf);
            pBuf = pNext;
        }
    }
}
