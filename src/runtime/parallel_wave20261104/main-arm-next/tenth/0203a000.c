#include "context.h"
void native_main_0203a000(PlayerHandle *handle, u32 value)
{
    if (!playerHandleValue(handle)) return;
    native_fn_0203a4fc(handle->player, value);
}
