#include "context.h"
void native_main_0209be60(DWCState state)
{
    stpDwcCnt->lastState = stpDwcCnt->state;
    stpDwcCnt->state = state;
}