#include "heap_views.h"

u32 native_main_0202b0f8(Heap *heap, u32 bytes, u32 alignment) {
    Block *block = heap->tail;
    Block *selected = 0;
    u32 start = 0;
    u32 smallest = 0xFFFFFFFF;
    u32 first = heap_mode(heap) == 0;
    while (block != 0) {
        u32 body = (u32)(block + 1);
        u32 aligned = (body + block->bytes - bytes) & ~(alignment - 1);
        if ((s32)(aligned - body) >= 0 && smallest > block->bytes) {
            selected = block;
            smallest = block->bytes;
            start = aligned;
            if (first || block->bytes == bytes) break;
        }
        block = block->previous;
    }
    if (selected == 0) return 0;
    return native_fn_0202ae9c(&heap->head, selected, start, bytes, 1);
}
