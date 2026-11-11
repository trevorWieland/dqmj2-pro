#include "context.h"

extern u32 native_data_021d18e4[];
extern void native_fn_0209aa64(u32 mode, u32 handle, u32 flag);

/* Release both queued handles of the shared state block. */
void native_main_02096b7c(void)
{
    if (native_data_021d18e4[1] != 0) {
        native_fn_0209aa64(1, native_data_021d18e4[1], 0);
        native_data_021d18e4[1] = 0;
    }
    if (native_data_021d18e4[0] != 0) {
        native_fn_0209aa64(1, native_data_021d18e4[0], 0);
        native_data_021d18e4[0] = 0;
    }
}
