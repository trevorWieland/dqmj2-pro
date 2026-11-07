#include "context.h"
BOOL native_main_020a3528 (BOOL sort)
{
    int eval;
    int deleteFlag = 0;
    int localDelete;
    int profileID;
    int i, j;
    SBServer server;

    for (i = 0; i < ServerBrowserCount(DWCi_GetMatchCnt()->sbObj); i++) {
        server = ServerBrowserGetServer(DWCi_GetMatchCnt()->sbObj, i);

        if (DWCi_GetMatchCnt()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
            profileID = SBServerGetIntValue(server, native_data_020e01f4, 0);
            localDelete = 0;
            for (j = 1; j <= DWCi_GetMatchCnt()->gt2NumConnection; j++) {
                if (profileID == DWCi_GetMatchCnt()->sbPidList[j]) {

                    ServerBrowserRemoveServer(DWCi_GetMatchCnt()->sbObj, server);

                    i--;
                    localDelete = 1;
                    break;
                }
            }

            if (localDelete) continue;
        }

        if (DWCi_GetMatchCnt()->evalCallback) {
            eval = DWCi_GetMatchCnt()->evalCallback(i, DWCi_GetMatchCnt()->evalParam);

            if (eval > 0) {
                if (eval > 0x007fffff) eval = 0x007fffff;
                SBServerAddIntKeyValue(server,
                                       native_data_020e0220,
                                       (int)((eval << 8) | DWCi_GetMathRand32(256)));
            } else {
                ServerBrowserRemoveServer(DWCi_GetMatchCnt()->sbObj, server);
                DWC_Printf(DWC_REPORTFLAG_SB_UPDATE,
                           "Deleted server [%d] (eval point is %d).\n",
                           i, eval);

                i--;
                deleteFlag = 1;
            }
        } else {
            SBServerAddIntKeyValue(server, native_data_020e0220,
                                   (int)DWCi_GetMathRand32(DWC_MAX_CONNECTIONS << 2));
        }
    }

    if (sort && ServerBrowserCount(DWCi_GetMatchCnt()->sbObj)) {
        ServerBrowserSort(DWCi_GetMatchCnt()->sbObj, SBFalse, native_data_020e0220, sbcm_int);
    }

    if (deleteFlag && !ServerBrowserCount(DWCi_GetMatchCnt()->sbObj)) return FALSE;
    else return TRUE;
}
