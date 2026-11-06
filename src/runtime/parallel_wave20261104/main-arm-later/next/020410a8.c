#include "context.h"
u32 native_main_020410a8(Heap58 *heap)
{
    u32 result=native_fn_02028af4(heap);
    if(heap->field0)native_fn_0202a51c(heap->field0);
    if(heap->field8)native_fn_0202a51c(heap->field8);
    native_fn_02008c58(0,heap,0x58);
    return result;
}
