#include "native_frame_core_types.h"
u32 native_main_0202b614(void *base,u32 bytes,u32 alignment) {
    Frame *frame=base;
    u32 previous=frame->tail;
    u32 extra=alignment-1;
    u32 aligned=(previous-bytes)&~extra;
    if (aligned<frame->head) return 0;
    {
        u16 options=frame_options(frame);
        u32 span=previous-aligned;
        if (options&1) {
            native_fn_02008c14(0,aligned,span);
        } else if (options&2) {
            native_fn_02008c14(native_fn_0202b9cc(1),aligned,span);
        }
    }
    frame->tail=aligned;
    return aligned;
}
