#include "initializer.h"
void native_main_0207154c(void)
{
    char path[32];
    ContextPrefix *context=native_fn_02061944();
    u32 amount;
    native_fn_0201d444(path,native_data_020de394);
    native_fn_0205ff80(path);
    amount=native_fn_02065730(&context->rows[1],59,0,2,context->cursor25c);
    context->cursor25c+=amount;
    native_fn_0205ff9c();
}
