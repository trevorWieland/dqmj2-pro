#include "context.h"
void native_main_0203a01c(PlayerHandle *handle, u32 frame, u32 extra)
{
    Player *player;
    if (!playerHandleValue(handle)) return;
    player = handle->player;
    if (player->flags110.bit3) return;
    native_fn_020379c4(player->timerDatae8, frame << 8, extra);
}
