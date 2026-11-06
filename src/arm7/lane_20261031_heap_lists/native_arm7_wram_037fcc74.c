#include "native_heap_types.h"
void* native_arm7_wram_037fcc74(OSArenaId id, OSHeapHandle heap, u32 size)
{
    OSHeapInfo* heapInfo;
    HeapDesc* hd;
    Cell* cell;
    Cell* newCell;
    long leftoverSize;

    OSIntrMode enabled = OS_DisableInterrupts();
    heapInfo = OSiHeapInfo[id];
    if (!heapInfo) {
        (void)OS_RestoreInterrupts(enabled);
        return NULL;
    }

    if (heap < 0) {
        heap = heapInfo->currentHeap;
    }

    hd = &heapInfo->heapArray[heap];

    size += HEADERSIZE;
    size = OSi_ROUND(size, 32);

    for (cell = hd->free; cell != NULL; cell = cell->next) {
        if ((long)size <= cell->size) {
            break;
        }
    }

    if (cell == NULL) {
        (void)OS_RestoreInterrupts(enabled);
        return NULL;
    }

    leftoverSize = cell->size - (long)size;
    if (leftoverSize < MINOBJSIZE) {
        hd->free = DLExtract(hd->free, cell);
    } else {
        cell->size = (long)size;

        newCell = (Cell *) ((char *)cell + size);
        newCell->size = leftoverSize;

        newCell->prev = cell->prev;
        newCell->next = cell->next;

        if (newCell->next != NULL) {
            newCell->next->prev = newCell;
        }

        if (newCell->prev != NULL) {
            newCell->prev->next = newCell;
        } else {
            hd->free = newCell;
        }
    }

    hd->allocated = DLAddFront(hd->allocated, cell);

    (void)OS_RestoreInterrupts(enabled);
    return (void *)((char *)cell + HEADERSIZE);
}
