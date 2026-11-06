#include "dependency000.h"

void native_utility_child_arm9_main_0200fa74 (int fifotag, PXIFifoCallback callback)
{
    OSIntrMode enabled;
    OSSystemWork * p = ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ;
    ((void) 0)                ;
    enabled = native_utility_child_arm9_arm_0200a64c();
    native_utility_child_arm9_data_0202cbcc[fifotag] = callback;
    if (callback) {
        p->pxiHandleChecker[PXI_PROC_ARM9 ] |= (1UL << fifotag);
    } else {
        p->pxiHandleChecker[PXI_PROC_ARM9 ] &= ~(1UL << fifotag);
    }
    (void)native_utility_child_arm9_arm_0200a660(enabled);
}
