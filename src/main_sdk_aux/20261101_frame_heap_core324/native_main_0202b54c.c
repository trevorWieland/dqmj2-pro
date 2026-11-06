#include "native_frame_core_types.h"
u32 native_main_0202b54c(void *base,u32 end,u32 options) {
    Heap *heap=base;
    native_fn_0202b914(heap,0x46524D48,(u32)heap+48,end,options);
    heap->frame.head=heap->common.begin;
    heap->frame.tail=heap->common.end;
    heap->frame.opaqueState=0;
    return (u32)heap;
}
