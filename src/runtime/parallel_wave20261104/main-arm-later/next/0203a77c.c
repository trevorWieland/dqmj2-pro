#include "context.h"
QueueNode *native_main_0203a77c(void *queue)
{
    u32 token=native_fn_02007ff4();
    QueueNode *node=native_fn_0202bb88(queue,0);
    if(node) {native_fn_0202bb28(queue,node);node->field8->field11c--;}
    native_fn_02008008(token);
    return node;
}
