#include "context.h"
u32 native_main_020911b0(ConnectionView *context)
{
    u32 flags=context->date_ok?0:0x8000;
    RootPrefix *root;
    void *hash;
    if(context->pub_algorithm==-1)return flags|4;
    switch(context->certificate_algorithm){
    case 3:
        hash=&context->md5tmp;
        native_fn_02092ffc(hash);
        native_fn_0209302c(hash,context->hash_start,context->hash_end-context->hash_start);
        native_fn_020930ac(hash,context->certificate_hash);
        context->certificate_hash_length=16;
        break;
    case 4:
        hash=&context->sha1tmp;
        native_fn_020936bc(hash);
        native_fn_020936f4(hash,context->hash_start,context->hash_end-context->hash_start);
        native_fn_02093774(hash,context->certificate_hash);
        context->certificate_hash_length=20;
        break;
    default:return flags|3;
    }
    root=native_fn_02090bdc(context,context->issuer);
    if(!root)return flags|1;
    return flags|native_fn_0209108c(context,root);
}
