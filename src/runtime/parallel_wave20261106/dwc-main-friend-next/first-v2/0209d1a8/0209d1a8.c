#include "context.h"
void native_main_0209d1a8 (void)
{
    if (stpFriendCnt) {
        stpFriendCnt->gpProcessCount = 0;
        stpFriendCnt->lastGpProcess = OS_GetTick();
    }
}
