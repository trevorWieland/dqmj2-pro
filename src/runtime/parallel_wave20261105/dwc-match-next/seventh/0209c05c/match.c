#include "context.h"
void native_main_0209c05c (DWCError error, BOOL cancel, BOOL self, BOOL isServer, int index, void * param)
{
#pragma unused(param)
    int i;

    if ((error == DWC_ERROR_NONE) && cancel) {

        if (stpDwcCnt->matchcnt.state == DWC_MATCH_STATE_INIT) {
            DWCi_ClearQR2Key();
            DWCi_SetState(DWC_STATE_ONLINE);
        }

    } else if (error == DWC_ERROR_NONE)   {
        DWCi_SetState(DWC_STATE_CONNECTED);

        for (i = 0; i <= stpDwcCnt->matchcnt.gt2NumConnection; i++) {
            if (stpDwcCnt->matchcnt.sbPidList[i] == stpDwcCnt->profileID) {
                stpDwcCnt->aid = stpDwcCnt->matchcnt.aidList[i];
                break;
            }
        }
    }

#ifndef SDK_FINALROM
    if (!error) {
        int i;

        for (i = 0; i < stpDwcCnt->matchcnt.gt2NumConnection + 1; i++) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "aid[%d] = %d, pid[%d] = %u\n",
                       i, stpDwcCnt->matchcnt.aidList[i],
                       i, stpDwcCnt->matchcnt.sbPidList[i]);
        }
    }
#endif

    stpDwcCnt->matchcnt.validAidBitmap =
        DWCi_GetAIDBitmapFromList(stpDwcCnt->matchcnt.aidList, stpDwcCnt->matchcnt.gt2NumConnection + 1);

    DWCi_SetNumValidConnection();

    if ((stpDwcCnt->matchcnt.qr2MatchType == DWC_MATCH_TYPE_SC_SV) ||
        (stpDwcCnt->matchcnt.qr2MatchType == DWC_MATCH_TYPE_SC_CL)) {
        stpDwcCnt->matchedSCCallback(error, cancel, self, isServer, index,
                                     stpDwcCnt->matchedSCParam);
    } else {
        stpDwcCnt->matchedCallback(error, cancel, stpDwcCnt->matchedParam);
    }

    if ((error != DWC_ERROR_NONE) &&
        (stpDwcCnt != NULL) && (stpDwcCnt->state == DWC_STATE_MATCHING)) {
        DWCi_SetState(DWC_STATE_ONLINE);
    }
}