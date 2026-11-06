#include "native_heap_types.h"
void *native_arm7_wram_037fce24(OSArenaId id, void *arenaStart, void *arenaEnd, s32 maxHeaps)
{
    OSIntrMode enabled = OS_DisableInterrupts();

    OSHeapInfo *heapInfo = arenaStart;
    OSiHeapInfo[id] = heapInfo;

    u32 arraySize = sizeof(HeapDesc) * maxHeaps;
    heapInfo->heapArray = (void *)((u32)arenaStart + sizeof(OSHeapInfo));
    heapInfo->numHeaps = maxHeaps;

    for (OSHeapHandle i = 0; i < heapInfo->numHeaps; i++)
    {
        HeapDesc *hd = &heapInfo->heapArray[i];

        hd->size = -1;
        hd->free = hd->allocated = NULL;
    }

    heapInfo->currentHeap = -1;

    arenaStart = (void *)((char *)heapInfo->heapArray + arraySize);
    arenaStart = (void *)OSi_ROUND(arenaStart, 32);

    heapInfo->arenaStart = arenaStart;
    heapInfo->arenaEnd = (void *)OSi_TRUNC(arenaEnd, 32);

    (void)OS_RestoreInterrupts(enabled);
    return heapInfo->arenaStart;
}
