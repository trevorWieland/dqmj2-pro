#include "cleanup_words.h"
u32 native_main_0205dbc4(u32 heap,u32 *holder) {
    u32 block=*holder;
    if (block==0) return 0;
    native_fn_0203cf9c(heap,block);
    *holder=0;
    return 1;
}
