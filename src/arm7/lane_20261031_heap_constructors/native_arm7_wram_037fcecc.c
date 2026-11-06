#include "native_heap_types.h"
OSHeapHandle native_arm7_wram_037fcecc(OSArenaId id, void *start, void *end)
{
    OSIntrMode enabled = OS_DisableInterrupts();

    OSHeapInfo *heapInfo = OSiHeapInfo[id];

    start = (void *)OSi_ROUND(start, 32);
    end = (void *)OSi_TRUNC(end, 32);

    for (OSHeapHandle heap = 0; heap < heapInfo->numHeaps; heap++)
    {
        HeapDesc *hd = &heapInfo->heapArray[heap];
        if (hd->size < 0)
        {
            hd->size = (s8 *)end - (s8 *)start;

            Cell *cell = (Cell *)start;
            cell->prev = NULL;
            cell->next = NULL;
            cell->size = hd->size;

            hd->free = cell;
            hd->allocated = 0;

            (void)OS_RestoreInterrupts(enabled);
            return heap;
        }
    }

    (void)OS_RestoreInterrupts(enabled);
    return -1;
}
