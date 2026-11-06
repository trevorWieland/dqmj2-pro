#include "native_dma_types.h"
void native_main_0200867c(u32 channel,const void *source,void *destination,u32 bytes,DmaCallback callback,u32 argument) {
    native_fn_020088a4(channel,source,bytes,0);
    if (bytes == 0) {
        if (callback == 0) {
            return;
        }
        callback(argument);
        return;
    }
    native_fn_02008714(channel);
    if (callback != 0) {
        native_fn_02005c64(channel,callback,argument);
        native_fn_01ff8448(channel,source,destination,(bytes >> 2) | 0xC4000000);
        return;
    }
    native_fn_01ff8448(channel,source,destination,(bytes >> 2) | 0x84000000);
}
