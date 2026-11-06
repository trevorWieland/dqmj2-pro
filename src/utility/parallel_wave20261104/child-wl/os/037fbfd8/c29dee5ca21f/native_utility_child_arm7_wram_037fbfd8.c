#include "dependency000.h"

s32 native_utility_child_arm7_wram_037fbfd8 (u16 lockID, OSLockWord * lockp, void (*ctrlFuncp)(void), BOOL disableFIQ)
{
    OSIntrMode lastInterrupts;
    ((void) 0) ;
    if (lockID != lockp->ownerID) {
        return (-2) ;
    }
    lastInterrupts = (disableFIQ) ? native_utility_child_arm7_arm_037fe448() : native_utility_child_arm7_arm_037fe41c();
    lockp->ownerID = 0;
    if (ctrlFuncp) {
        ctrlFuncp();
    }
    lockp->lockFlag = 0;
    if (disableFIQ) {
        (void)native_utility_child_arm7_arm_037fe45c(lastInterrupts);
    } else {
        (void)native_utility_child_arm7_arm_037fe430(lastInterrupts);
    }
    return 0 ;
}
