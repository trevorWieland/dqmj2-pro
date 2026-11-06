#include "context.h"
void native_main_0203a050(PlayerHandle *handle, u32 value, u32 extra)
{
    if (!playerHandleValue(handle)) return;
    native_fn_0203b8dc(handle->player, value, extra);
}
