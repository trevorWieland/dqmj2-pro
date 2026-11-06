#include "native_thread_types.h"
u32 native_main_020067fc(NativeThread *thread) {
    u32 previous = native_fn_02007ff4();
    if (NATIVE_CURRENT_THREAD == thread) {
        native_fn_020067a0();
    }
    native_fn_02006c70();
    native_fn_0200716c(thread);
    native_fn_02006878(thread);
    if (thread->waitingQueue != 0) {
        native_fn_020062a4(thread->waitingQueue,thread);
    }
    native_fn_02006388(thread);
    thread->state = 2;
    native_fn_02006924(&thread->joinQueue);
    native_fn_02006ca4();
    native_fn_02008008(previous);
    return native_fn_020069dc();
}
