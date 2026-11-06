#include "context_00.h"
void native_main_02006ab0 (OSThread * thread, u32 offset)
{
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0)
                  ;
    thread->stackWarningOffset = offset;
    if (offset != 0) {
        *(u32 *)(thread->stackTop + offset) = 0x597dfbd9UL ;
    }
}
