#include "native_heap_types.h"
void native_arm7_wram_037fcd84(OSArenaId id, OSHeapHandle heap, void* ptr)
{
    OSHeapInfo *heapInfo;
    HeapDesc *hd;
    Cell   *cell;

    OSIntrMode enabled = OS_DisableInterrupts();
    heapInfo = OSiHeapInfo[id];

    if (heap < 0) {
        heap = heapInfo->currentHeap;
    }

    cell = (Cell *) ((char *)ptr - HEADERSIZE);
    hd = &heapInfo->heapArray[heap];

    hd->allocated = DLExtract(hd->allocated, cell);
    hd->free = DLInsert(hd->free, cell);

    (void)OS_RestoreInterrupts(enabled);
}
