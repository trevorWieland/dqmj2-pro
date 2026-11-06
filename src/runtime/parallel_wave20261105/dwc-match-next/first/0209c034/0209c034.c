#include "context.h"
void native_main_0209c034(DWCError error, BOOL isChanged, void * param)
{
#pragma unused(param)

    if (stpDwcCnt->lastState != DWC_STATE_UPDATE_SERVERS) {

        DWCi_SetState(stpDwcCnt->lastState);
    }

    stpDwcCnt->updateServersCallback(error, isChanged, stpDwcCnt->updateServersParam);
}