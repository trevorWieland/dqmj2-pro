#include "native_frame_core_types.h"
u32 native_main_0202b594(void *base,u32 bytes,u32 alignment) {
    Frame *frame=base;
    u32 previous=frame->head;
    u32 extra=alignment-1;
    u32 aligned=(extra+previous)&~extra;
    u32 finish=bytes+aligned;
    if (finish>frame->tail) return 0;
    {
        u16 options=frame_options(frame);
        u32 span=finish-previous;
        if (options&1) {
            native_fn_02008c14(0,previous,span);
        } else if (options&2) {
            native_fn_02008c14(native_fn_0202b9cc(1),previous,span);
        }
    }
    frame->head=finish;
    return aligned;
}
