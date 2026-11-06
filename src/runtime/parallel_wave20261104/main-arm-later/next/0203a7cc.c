#include "context.h"
QueueNode *native_main_0203a7cc(void)
{
    u32 token=native_fn_02007ff4();
    QueueNode *node=native_fn_0202bb88(native_data_020f4c90,0);
    if(node)native_fn_0202bb28(native_data_020f4c90,node);
    native_fn_02008008(token);
    return node;
}
