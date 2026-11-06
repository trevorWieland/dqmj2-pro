#include "context.h"
void native_main_02091afc(ConnectionView *context,u8 *output,s32 direction)
{
    u8 padding[40];
    void *hash=&context->sha1live;
    if(context->server^direction)native_fn_020936f4(hash,native_data_020de888,4);
    else native_fn_020936f4(hash,native_data_020de890,4);
    native_fn_020936f4(hash,context->master,48);
    native_fn_02008d78(padding,0x36,40);
    native_fn_020936f4(hash,padding,40);
    native_fn_02093774(hash,output);
    native_fn_020936bc(hash);
    native_fn_020936f4(hash,context->master,48);
    native_fn_02008d78(padding,0x5c,40);
    native_fn_020936f4(hash,padding,40);
    native_fn_020936f4(hash,output,20);
    native_fn_02093774(hash,output);
}
