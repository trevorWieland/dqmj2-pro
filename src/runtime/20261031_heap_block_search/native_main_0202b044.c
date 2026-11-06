#include "heap_views.h"

u32 native_main_0202b044(Heap *heap, u32 bytes, u32 alignment) {
    Block *block = heap->head;
    Block *selected = 0;
    u32 start = 0;
    u32 smallest = 0xFFFFFFFF;
    u32 first = heap_mode(heap) == 0;
    while (block != 0) {
        u32 body = (u32)(block + 1);
        u32 aligned = (body + alignment - 1) & ~(alignment - 1);
        u32 needed = bytes + (aligned - body);
        if (block->bytes >= needed && smallest > block->bytes) {
            selected = block;
            smallest = block->bytes;
            start = aligned;
            if (first || block->bytes == bytes) break;
        }
        block = block->next;
    }
    if (selected == 0) return 0;
    return native_fn_0202ae9c(&heap->head, selected, start, bytes, 0);
}
