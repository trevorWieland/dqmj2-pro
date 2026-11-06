#include "context.h"
s32 native_main_02091de0(ConnectionView *context,u8 *input)
{
    void *hash;
    u8 padding[48];
    s32 length=(input[3]<<8)+input[4];
    u8 *payload=input+5;
    switch(context->method){
    case 4:
        hash=&context->md5tmp;
        native_fn_02092ffc(hash);
        native_fn_0209302c(hash,context->send_secret,16);
        native_fn_02008d78(padding,0x36,48);
        native_fn_0209302c(hash,padding,48);
        native_fn_0209302c(hash,context->send_sequence,8);
        native_fn_0209302c(hash,input,1);
        native_fn_0209302c(hash,input+3,length+2);
        native_fn_020930ac(hash,payload+length);
        native_fn_02092ffc(hash);
        native_fn_0209302c(hash,context->send_secret,16);
        native_fn_02008d78(padding,0x5c,48);
        native_fn_0209302c(hash,padding,48);
        native_fn_0209302c(hash,payload+length,16);
        native_fn_020930ac(hash,payload+length);
        length+=16;
        break;
    case 5:
        hash=&context->sha1tmp;
        native_fn_020936bc(hash);
        native_fn_020936f4(hash,context->send_secret,20);
        native_fn_02008d78(padding,0x36,40);
        native_fn_020936f4(hash,padding,40);
        native_fn_020936f4(hash,context->send_sequence,8);
        native_fn_020936f4(hash,input,1);
        native_fn_020936f4(hash,input+3,length+2);
        native_fn_02093774(hash,payload+length);
        native_fn_020936bc(hash);
        native_fn_020936f4(hash,context->send_secret,20);
        native_fn_02008d78(padding,0x5c,40);
        native_fn_020936f4(hash,padding,40);
        native_fn_020936f4(hash,payload+length,20);
        native_fn_02093774(hash,payload+length);
        length+=20;
        break;
    }
    input[3]=length>>8;input[4]=length;
    native_fn_02093824(context->send_cipher,input+5,length);
    native_fn_02091c30(context->send_sequence+8);
    return length+5;
}
