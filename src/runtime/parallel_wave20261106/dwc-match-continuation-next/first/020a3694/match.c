#include "context.h"
void native_main_020a3694 (void)
{
    u32 rand;
    int tmpEval, maxEval = 0;
    int sum = 0;
    int i;
    int eval[DWC_SB_UPDATE_MAX_SERVERS];
    SBServer server;

    if (ServerBrowserCount(DWCi_GetMatchCnt()->sbObj) <= 1) return;

    for (i = 0; i < ServerBrowserCount(DWCi_GetMatchCnt()->sbObj); i++) {
        server = ServerBrowserGetServer(DWCi_GetMatchCnt()->sbObj, i);
        tmpEval = SBServerGetIntValue(server, native_data_020e0220, -1);
        if (tmpEval > maxEval) maxEval = tmpEval;

        sum += stEvalRate[i];
    }

    rand = DWCi_GetMathRand32(100);

    for (i = 0; i < ServerBrowserCount(DWCi_GetMatchCnt()->sbObj); i++) {
        if (i == ServerBrowserCount(DWCi_GetMatchCnt()->sbObj) - 1) {
            eval[i] = 100;
            break;
        } else {
            eval[i] = (100 * stEvalRate[i]) / sum + (i > 0 ? eval[i - 1] : 0);
            if (rand < eval[i]) break;
        }
    }

    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "Server[%d] is selected (%d/100: rand %d)\n",
               i, eval[i], rand);

    if (maxEval < 0x7fffffff) maxEval++;
    SBServerAddIntKeyValue(ServerBrowserGetServer(DWCi_GetMatchCnt()->sbObj, i),
                           native_data_020e0220,
                           maxEval);

    ServerBrowserSort(DWCi_GetMatchCnt()->sbObj, SBFalse, native_data_020e0220, sbcm_int);
}
