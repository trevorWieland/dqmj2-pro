#include "dependency000.h"
#include "dependency001.h"

u32 native_utility_child_arm7_wram_037f8918(LPHEAPBUF_MAN pBufMan, void *pBuf)
{
    LPHEAPBUF_HEADER pBufHeader = (LPHEAPBUF_HEADER)pBuf;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan;
    u32 sts;
    { if (pBufHeader->BufID != 0xBF1D) return 1; } ;
    sts = native_utility_child_arm7_arm_037f878c(pBufMan, pBufHeader);
    if (sts) {
        goto release_err;
    }
    switch (pHeapMan->HeapInfo.heapType) {
    case 0 :
        native_utility_child_arm7_arm_037fd484(pHeapMan->HeapInfo.func.os.id, pHeapMan->HeapInfo.func.os.heapHandle, pBufHeader);
        break;
    case 1 :
        (*pHeapMan->HeapInfo.func.ext.free)(pBufHeader);
        break;
    }
release_err:
    return sts;
}
#include "dependency002.h"
