#include "context.h"
void native_main_02091a68(ConnectionView *context,u8 *output,s32 direction)
{
    u8 padding[48];
    void *hash=&context->md5live;
    if(context->server^direction)native_fn_0209302c(hash,native_data_020de888,4);
    else native_fn_0209302c(hash,native_data_020de890,4);
    native_fn_0209302c(hash,context->master,48);
    native_fn_02008d78(padding,0x36,48);
    native_fn_0209302c(hash,padding,48);
    native_fn_020930ac(hash,output);
    native_fn_02092ffc(hash);
    native_fn_0209302c(hash,context->master,48);
    native_fn_02008d78(padding,0x5c,48);
    native_fn_0209302c(hash,padding,48);
    native_fn_0209302c(hash,output,16);
    native_fn_020930ac(hash,output);
}
