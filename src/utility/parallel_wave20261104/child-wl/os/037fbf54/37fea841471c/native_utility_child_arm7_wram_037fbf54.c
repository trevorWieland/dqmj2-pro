#include "dependency000.h"

s32 native_utility_child_arm7_wram_037fbf54 (u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFIQ)
{
    s32 lastLockFlag;
    OSIntrMode lastInterrupts;
    ((void) 0) ;
    lastInterrupts = (disableFIQ) ? native_utility_child_arm7_arm_037fe448() : native_utility_child_arm7_arm_037fe41c();
    lastLockFlag = (s32)native_utility_child_arm7_arm_037fe944(lockID, &lockp->lockFlag);
    if (lastLockFlag == 0 ) {
        if (ctrlFuncp) {
            ctrlFuncp();
        }
        lockp->ownerID = lockID;
    }
    if (disableFIQ) {
        (void)native_utility_child_arm7_arm_037fe45c(lastInterrupts);
    } else {
        (void)native_utility_child_arm7_arm_037fe430(lastInterrupts);
    }
    return lastLockFlag;
}
