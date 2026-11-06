#include "context_00.h"
s32 native_main_02005eac (u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFiq)
{
    s32 lastLockFlag;
    while ((lastLockFlag = native_fn_02005f8c(lockID, lockp, ctrlFuncp, disableFiq)) > 0 ) {
        OSi_WaitByLoop();
    }
    return lastLockFlag;
}
