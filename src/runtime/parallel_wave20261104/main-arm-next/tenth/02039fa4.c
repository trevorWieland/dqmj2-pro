#include "context.h"
void native_main_02039fa4(PlayerHandle *handle)
{
    if (!playerHandleValue(handle)) return;
    handle->player->flags110.bit2 = 1;
}
