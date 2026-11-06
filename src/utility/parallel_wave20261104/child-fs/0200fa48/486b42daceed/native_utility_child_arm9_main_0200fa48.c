#include "dependency000.h"

BOOL native_utility_child_arm9_main_0200fa48 (int fifotag, PXIProc proc)
{
    OSSystemWork * p = ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ;
    return (p->pxiHandleChecker[proc] & (1UL << fifotag)) ? 1 : 0 ;
}
