#include "context.h"

/* Fire the transfer completion queued in the control block.  The pending count
   is cleared even when no callback is installed. */
void native_main_0200e4d4(u32 value)
{
    void (*callback)(u32, u32) = native_data_020e540c.callback;
    u32 arg = native_data_020e540c.callback_arg;

    native_data_020e540c.pending = 0;
    if (callback != 0) {
        native_data_020e540c.callback = 0;
        callback(value, arg);
    }
}

