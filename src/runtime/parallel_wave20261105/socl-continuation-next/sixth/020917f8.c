#include "context.h"
void native_main_020917f8(u8 *destination,char *salt,ConnectionView *context)
{
    u8 temporary[20];
    void *hash;
    hash=&context->sha1tmp;
    native_fn_020936bc(hash);
    native_fn_020936f4(hash,salt,native_fn_0201d69c(salt));
    native_fn_020936f4(hash,context->master,48);
    native_fn_020936f4(hash,context->randoms,64);
    native_fn_02093774(hash,temporary);
    hash=&context->md5tmp;
    native_fn_02092ffc(hash);
    native_fn_0209302c(hash,context->master,48);
    native_fn_0209302c(hash,temporary,20);
    native_fn_020930ac(hash,destination);
}
