#include "context.h"
SBError native_main_0209fc38 (int profileID)
{
    char filter[MAX_FILTER_LEN];
    char * pFilter = filter;
    u8 basicFields[DWC_NUM_QR2_MATCH_KEY + DWC_QR2_GAME_RESERVED_KEYS];
    int len;
    int numBasicFields = DWC_NUM_QR2_MATCH_KEY;
    int i;
    SBError sbError = sbe_noerror;
    basicFields[0] = NUMPLAYERS_KEY;
    basicFields[1] = MAXPLAYERS_KEY;
    basicFields[2] = DWC_QR2_PID_KEY;
    basicFields[3] = DWC_QR2_MATCH_TYPE_KEY;
    basicFields[4] = DWC_QR2_MATCH_RESV_KEY;
    basicFields[5] = DWC_QR2_MATCH_VER_KEY;
    basicFields[6] = DWC_QR2_MATCH_EVAL_KEY;
    if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) ||
        (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)) {
        for (i = 0; i < DWC_QR2_GAME_RESERVED_KEYS; i++) {
            if (native_data_021d1ba8[i].keyID) {
                basicFields[numBasicFields] = native_data_021d1ba8[i].keyID;
                numBasicFields++;
            }
        }
    }
    switch (native_fn_020a3d70()->state) {
    case DWC_MATCH_STATE_CL_SEARCH_HOST:
        if (!native_fn_020a3d70()->priorProfileID) {
            len = native_fn_0209fda4(filter, native_fn_020a3d70()->profileID,
                                             native_fn_020a3d70()->qr2NumEntry,
                                             native_fn_020a3d70()->qr2MatchType);
            if (stpAddFilter) {
                (void)native_fn_020061ac(&filter[len], sizeof(filter) - len,
                                  native_data_020e022c,
                                  stpAddFilter);
            }
            break;
        } else {
            profileID = native_fn_020a3d70()->priorProfileID;
        }
    case DWC_MATCH_STATE_CL_SEARCH_OWN:
    case DWC_MATCH_STATE_CL_WAIT_RESV:
    case DWC_MATCH_STATE_CL_SEARCH_NN_HOST:
        (void)native_fn_020061ac(filter, sizeof(filter),
                          native_data_020e0238,
                          DWC_QR2_PID_KEY_STR, profileID);
        native_fn_020a3d70()->reqProfileID = profileID;
        break;
    default:
        DWC_Printf(DWC_REPORTFLAG_ERROR,
                   "---DWCi_SBUpdateAsync() illegal state %d.\n",
                   native_fn_020a3d70()->state);
    }
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "ServerBrowserFilter : %s\n", filter);
    native_fn_020a6964(native_fn_020a3d70()->sbObj);
    for (i = 0; i < DWC_DNS_ERROR_RETRY_MAX; i++) {
        sbError = native_fn_020a6898(native_fn_020a3d70()->sbObj, SBTrue, SBFalse,
                                           basicFields, numBasicFields,
                                           filter, DWC_SB_UPDATE_MAX_SERVERS);
        if (!sbError) break;
        else if (sbError != sbe_dnserror) break;
    }
    if (!sbError) {
        native_fn_020a3d70()->sbUpdateRequestTick = native_fn_02007a9c() + OS_MilliSecondsToTicks(DWC_SB_UPDATE_TIMEOUT);
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "ServerBrowserLimitUpdate timeout set.(%s)\n", __FUNCTION__);
    }
    return sbError;
}
