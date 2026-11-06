#include "context_00.h"
void native_main_020076ec (OSArenaId id, void * newHi)
{
    ((void) 0) ;
    ((void) 0) ;
    (*(OSArenaInfo *)(0x02000000 + 0x007ffda0)) .hi[id] = newHi;
}
