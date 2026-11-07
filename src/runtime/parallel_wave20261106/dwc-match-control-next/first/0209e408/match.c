#include "context.h"
void native_main_0209e408 (qr2_t qr2Obj)
{
    if (qr2Obj == NULL) {
        return;
    }

    qr2_think(qr2Obj);

    if (qr2Obj->userstatechangerequested) {
        return;
    }

    switch (DWCi_GetMatchCnt()->qr2MatchType) {
    case DWC_MATCH_TYPE_ANYBODY:
    case DWC_MATCH_TYPE_FRIEND:
        switch (DWCi_GetMatchCnt()->state) {
        case DWC_MATCH_STATE_CL_WAITING:
        case DWC_MATCH_STATE_CL_SEARCH_OWN:
        case DWC_MATCH_STATE_CL_SEARCH_HOST:
        case DWC_MATCH_STATE_CL_WAIT_RESV:
        case DWC_MATCH_STATE_CL_NN:
        case DWC_MATCH_STATE_SV_OWN_NN:
            qr2_send_statechanged(DWCi_GetMatchCnt()->qr2Obj);
            break;
        }
        break;
    case DWC_MATCH_TYPE_SC_SV:
        if (DWCi_GetMatchCnt()->state == DWC_MATCH_STATE_SV_OWN_NN) {
            qr2_send_statechanged(DWCi_GetMatchCnt()->qr2Obj);
        }
        break;
    }
}
