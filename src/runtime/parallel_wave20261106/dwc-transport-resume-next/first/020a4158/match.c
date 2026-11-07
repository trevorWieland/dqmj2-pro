#include "context.h"
BOOL native_main_020a4158 (u8 aid, u32 time)
{
    if (!sTransInfo) return FALSE;

    sTransInfo->connections[aid].recvTimeoutTime = time;
    sTransInfo->connections[aid].previousRecvTick = OS_GetTick();

    return TRUE;
}
