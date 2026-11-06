#include "context.h"
void native_main_0209d4e0(DWCFriendData friendData[], int deleteIndex, int otherIndex)
{
    if (stpFriendCnt) {
        MI_CpuClear8(&friendData[deleteIndex], sizeof(DWCFriendData));

        if (stpFriendCnt->deleteCallback) {
            stpFriendCnt->deleteCallback(deleteIndex, otherIndex,
                                         stpFriendCnt->deleteParam);
        }
    }
}