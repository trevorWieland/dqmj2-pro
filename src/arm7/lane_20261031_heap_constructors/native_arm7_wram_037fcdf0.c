#include "native_heap_types.h"
OSHeapHandle native_arm7_wram_037fcdf0(OSArenaId id, OSHeapHandle heap)
{
    OSIntrMode enabled = OS_DisableInterrupts();

    OSHeapInfo *heapInfo = OSiHeapInfo[id];
    OSHeapHandle prev = heapInfo->currentHeap;
    heapInfo->currentHeap = heap;

    (void)OS_RestoreInterrupts(enabled);
    return prev;
}
