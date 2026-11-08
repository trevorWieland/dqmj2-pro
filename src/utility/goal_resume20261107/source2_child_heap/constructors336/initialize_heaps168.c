#include "heap_types.h"

extern HeapSelection *native_utility_child_arm7_data_03805b30[];
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32 irqMask);

void *native_utility_child_arm7_wram_037fd3a0(u32 arenaSlot, void *metadataStart, void *end, s32 maxHeaps)
{
    u32 irqMask;
    HeapArena *arena;
    HeapDescriptor *descriptor;
    u32 descriptorBytes;
    s32 heapIndex;

    irqMask = native_utility_child_arm7_arm_037fe41c();
    arena = (HeapArena *)metadataStart;
    native_utility_child_arm7_data_03805b30[arenaSlot] = &arena->selection;
    descriptorBytes = (u32)maxHeaps * 12U;
    arena->descriptors = (HeapDescriptor *)((u32)metadataStart + 20U);
    arena->heapCount = maxHeaps;
    for (heapIndex = 0; heapIndex < arena->heapCount; heapIndex++) {
        descriptor = &arena->descriptors[heapIndex];
        descriptor->totalBytes = -1;
        descriptor->allocatedHead = 0;
        descriptor->freeHead = descriptor->allocatedHead;
    }
    arena->selection.currentHeap = -1;
    arena->arenaStart = (u8 *)(((u32)arena->descriptors + descriptorBytes + 31U) & ~31U);
    arena->arenaEnd = (u8 *)((u32)end & ~31U);
    native_utility_child_arm7_arm_037fe430(irqMask);
    return arena->arenaStart;
}
