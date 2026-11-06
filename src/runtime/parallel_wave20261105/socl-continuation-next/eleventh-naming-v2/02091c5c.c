#include "context.h"
s32 native_main_02091c5c(ConnectionView *context,u8 *input)
{
    s32 hash_length;
    void *hash;
    u8 digest[20];
    u8 padding[48];
    s32 length;
    length=native_fn_02091c48(context,input+5,(input[3]<<8)+input[4]);
    switch(context->method){
    case 4:
        length-=16;input[3]=length>>8;input[4]=length;
        hash=&context->md5tmp;
        native_fn_02092ffc(hash);
        native_fn_0209302c(hash,context->receive_secret,16);
        native_fn_02008d78(padding,0x36,48);
        native_fn_0209302c(hash,padding,48);
        native_fn_0209302c(hash,context->sequence,8);
        native_fn_0209302c(hash,input,1);
        native_fn_0209302c(hash,input+3,length+2);
        native_fn_020930ac(hash,digest);
        native_fn_02092ffc(hash);
        native_fn_0209302c(hash,context->receive_secret,16);
        native_fn_02008d78(padding,0x5c,48);
        native_fn_0209302c(hash,padding,48);
        native_fn_0209302c(hash,digest,16);
        native_fn_020930ac(hash,digest);
        hash_length=16;
        break;
    case 5:
        length-=20;input[3]=length>>8;input[4]=length;
        hash=&context->sha1tmp;
        native_fn_020936bc(hash);
        native_fn_020936f4(hash,context->receive_secret,20);
        native_fn_02008d78(padding,0x36,40);
        native_fn_020936f4(hash,padding,40);
        native_fn_020936f4(hash,context->sequence,8);
        native_fn_020936f4(hash,input,1);
        native_fn_020936f4(hash,input+3,length+2);
        native_fn_02093774(hash,digest);
        native_fn_020936bc(hash);
        native_fn_020936f4(hash,context->receive_secret,20);
        native_fn_02008d78(padding,0x5c,40);
        native_fn_020936f4(hash,padding,40);
        native_fn_020936f4(hash,digest,20);
        native_fn_02093774(hash,digest);
        hash_length=20;
        break;
    }
    if(native_fn_0201b248(input+5+length,digest,hash_length))context->state=9;
    native_fn_02091c30(context->sequence+8);
    return length+5;
}
