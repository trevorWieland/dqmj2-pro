#include "native_heap_family_types.h"
u32 native_main_0202b044(Heap *heap,u32 bytes,s32 alignment) {
    ExpHeap *exp = &heap->exp;
    const BOOL first = heap_mode(exp) == 0;
    Block *block = exp->free.head;
    Block *selected = NULL;
    u32 smallest = 0xFFFFFFFF;
    u32 start = 0;
    if (block != NULL) {
        u32 alignmentExtra = alignment - 1;
        u32 alignmentMask = ~alignmentExtra;
        do {
            const u32 body = (u32)(block + 1);
            const u32 aligned = (alignmentExtra + body) & alignmentMask;
            const u32 offset = aligned - body;
            if (block->bytes >= bytes + offset && smallest > block->bytes) {
                selected = block;
                smallest = block->bytes;
                start = aligned;
                if (first || smallest == bytes) {
                    break;
                }
            }
            block = block->next;
        } while (block != NULL);
    }
    if (selected == NULL) {
        return 0;
    }
    return native_fn_0202ae9c(exp,selected,start,bytes,0);
}
