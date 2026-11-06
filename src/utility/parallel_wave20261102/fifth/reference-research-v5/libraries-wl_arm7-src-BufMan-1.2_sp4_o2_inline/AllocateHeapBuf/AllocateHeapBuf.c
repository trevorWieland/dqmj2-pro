#include "context000.h"

#include "context001.h"

void *AllocateHeapBuf(LPHEAPBUF_MAN pBufMan, u32 Length)
{
    u32 AllocPages;
    LPHEAPBUF_HEADER pAllocBuf;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan;
    if (Length == 0) {
        return (void *)(0) ;
    }
    AllocPages = Length + sizeof(HEAPBUF_HEADER);
    switch (pHeapMan->HeapInfo.heapType) {
    case 0 :
        pAllocBuf = (LPHEAPBUF_HEADER)OS_AllocFromHeap(pHeapMan->HeapInfo.func.os.id, pHeapMan->HeapInfo.func.os.heapHandle, AllocPages);
        break;
    case 1 :
        pAllocBuf = (LPHEAPBUF_HEADER)(*pHeapMan->HeapInfo.func.ext.alloc)(AllocPages);
        break;
    }
    if (pAllocBuf != 0 ) {
        pAllocBuf->BufID = 0xBF1D ;
        pAllocBuf->Flag = 0x00 ;
        AddHeapBuf(pBufMan, pAllocBuf);
        return (void *)pAllocBuf;
    }
    return 0 ;
}

#include "context002.h"
