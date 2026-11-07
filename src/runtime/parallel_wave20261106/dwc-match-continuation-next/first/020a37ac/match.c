#include "context.h"
void native_main_020a37ac (int keyid, qr2_buffer_t outbuf, void * userdata)
{
#pragma unused(userdata)
    int index;

    switch (keyid) {
    case NUMPLAYERS_KEY:
        qr2_buffer_add_int(outbuf, DWCi_GetMatchCnt()->qr2NNFinishCount);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, DWCi_GetMatchCnt()->qr2NNFinishCount);
        break;
    case MAXPLAYERS_KEY:
        qr2_buffer_add_int(outbuf, DWCi_GetMatchCnt()->qr2NumEntry);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, DWCi_GetMatchCnt()->qr2NumEntry);
        break;
    case DWC_QR2_PID_KEY:
        qr2_buffer_add_int(outbuf, DWCi_GetMatchCnt()->profileID);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, DWCi_GetMatchCnt()->profileID);
        break;
    case DWC_QR2_MATCH_TYPE_KEY:
        qr2_buffer_add_int(outbuf, DWCi_GetMatchCnt()->qr2MatchType);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, DWCi_GetMatchCnt()->qr2MatchType);
        break;
    case DWC_QR2_MATCH_RESV_KEY:
        qr2_buffer_add_int(outbuf, DWCi_GetMatchCnt()->qr2Reservation);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, DWCi_GetMatchCnt()->qr2Reservation);
        break;
    case DWC_QR2_MATCH_VER_KEY:
        qr2_buffer_add_int(outbuf, DWC_MATCHING_VERSION);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, DWC_MATCHING_VERSION);
        break;
    case DWC_QR2_MATCH_EVAL_KEY:
        qr2_buffer_add_int(outbuf, 1);
        DWC_Printf(DWC_REPORTFLAG_QR2_REQ, "QR2, Received ServerKeyReq : keyID %d - %d\n", keyid, 1);
        break;
    default:
        index = keyid - DWC_QR2_GAME_KEY_START;
        if ((index >= 0 && index < DWC_QR2_GAME_RESERVED_KEYS)
            && stGameMatchKeys[index].keyID) {
            if (stGameMatchKeys[index].isStr) {
                qr2_buffer_add(outbuf, (char *)stGameMatchKeys[index].value);
            } else {
                qr2_buffer_add_int(outbuf, *(int *)stGameMatchKeys[index].value);
            }
        }
        break;
    }
}
