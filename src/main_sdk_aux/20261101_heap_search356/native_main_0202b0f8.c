#include "native_heap_family_types.h"
u32 native_main_0202b0f8(Heap *heap,u32 bytes,s32 alignment) {
    ExpHeap *exp = &heap->exp;
    const BOOL first = heap_mode(exp) == 0;
    Block *block = exp->free.tail;
    Block *selected = NULL;
    u32 smallest = 0xFFFFFFFF;
    u32 start = 0;
    if (block != NULL) {
        u32 alignmentMask = ~(alignment - 1);
        do {
            const u32 body = (u32)(block + 1);
            const u32 aligned = (block->bytes + body - bytes) & alignmentMask;
            const s32 offset = (s32)(aligned - body);
            if (offset >= 0 && smallest > block->bytes) {
                selected = block;
                smallest = block->bytes;
                start = aligned;
                if (first || smallest == bytes) {
                    break;
                }
            }
            block = block->previous;
        } while (block != NULL);
    }
    if (selected == NULL) {
        return 0;
    }
    return native_fn_0202ae9c(exp,selected,start,bytes,1);
}
