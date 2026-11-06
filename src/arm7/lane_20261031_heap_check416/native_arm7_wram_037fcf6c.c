#include "native_heap_types.h"
s32 native_arm7_wram_037fcf6c(OSArenaId id, OSHeapHandle heap)
{
    OSHeapInfo *heapInfo;
    HeapDesc *hd;
    Cell *cell;
    s32 total = 0;
    s32 free = 0;
    s32 retValue = -1;
    OSIntrMode enabled = OS_DisableInterrupts();

    heapInfo = OSiHeapInfo[id];

    if (heap == (OSHeapHandle)-1)
    {
        heap = heapInfo->currentHeap;
    }

    OSi_CHECK(heapInfo->heapArray);
    OSi_CHECK(0 <= heap && heap < heapInfo->numHeaps);

    hd = &heapInfo->heapArray[heap];
    OSi_CHECK(0 <= hd->size);

    OSi_CHECK(hd->allocated == NULL || hd->allocated->prev == NULL);
    for (cell = hd->allocated; cell; cell = cell->next)
    {
        OSi_CHECK(OSi_InRange(cell, heapInfo->arenaStart, heapInfo->arenaEnd));
        OSi_CHECK(OSi_OFFSET(cell, 32) == 0);
        OSi_CHECK(cell->next == NULL || cell->next->prev == cell);
        OSi_CHECK(MINOBJSIZE <= cell->size);
        OSi_CHECK(OSi_OFFSET(cell->size, 32) == 0);

        total += cell->size;
        OSi_CHECK(0 < total && total <= hd->size);
    }

    OSi_CHECK(hd->free == NULL || hd->free->prev == NULL);
    for (cell = hd->free; cell; cell = cell->next)
    {
        OSi_CHECK(OSi_InRange(cell, heapInfo->arenaStart, heapInfo->arenaEnd));
        OSi_CHECK(OSi_OFFSET(cell, 32) == 0);
        OSi_CHECK(cell->next == NULL || cell->next->prev == cell);
        OSi_CHECK(MINOBJSIZE <= cell->size);
        OSi_CHECK(OSi_OFFSET(cell->size, 32) == 0);
        OSi_CHECK(cell->next == NULL || (s8 *)cell + cell->size < (s8 *)cell->next);

        total += cell->size;
        free += cell->size - HEADERSIZE;

        OSi_CHECK(0 < total && total <= hd->size);
    }

    OSi_CHECK(total == hd->size);
    retValue = free;

exit_OS_CheckHeap:
    (void)OS_RestoreInterrupts(enabled);
    return retValue;
}
