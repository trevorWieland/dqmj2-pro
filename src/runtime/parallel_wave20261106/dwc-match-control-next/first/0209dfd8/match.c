#include "context.h"
qr2_error_t native_main_0209dfd8 (int profileID)
{
    int i;
    qr2_error_t qr2Error = e_qrnoerror;

    if (DWCi_GetMatchCnt()->qr2Obj) {
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "QR2 is already set up.\n");
        return e_qrnoerror;
    }

    DWCi_GetMatchCnt()->profileID = profileID;

    for (i = 0; i < DWC_DNS_ERROR_RETRY_MAX; i++) {
        qr2Error = qr2_init_socket(&DWCi_GetMatchCnt()->qr2Obj,
                                   gt2GetSocketSOCKET(*DWCi_GetMatchCnt()->pGt2Socket),
                                   gt2GetLocalPort(*DWCi_GetMatchCnt()->pGt2Socket),
                                   DWCi_GetMatchCnt()->gameName, DWCi_GetMatchCnt()->secretKey, 1, 1,
                                   DWCi_QR2ServerKeyCallback,
                                   DWCi_QR2PlayerKeyCallback,
                                   DWCi_QR2TeamKeyCallback,
                                   DWCi_QR2KeyListCallback,
                                   DWCi_QR2CountCallback,
                                   DWCi_QR2AddErrorCallback,
                                   NULL);
        if (!qr2Error) break;
        else {
            qr2_shutdown(DWCi_GetMatchCnt()->qr2Obj);
            DWCi_GetMatchCnt()->qr2Obj = NULL;
        }

        if ((qr2Error != e_qrdnserror) || (i == DWC_DNS_ERROR_RETRY_MAX - 1)) {
            DWCi_HandleQR2Error(qr2Error);
            return qr2Error;
        }
    }

#ifdef DWC_QR2_ALIVE_DURING_MATCHING
    DWCi_GetMatchCnt()->qr2IP = 0;
    DWCi_GetMatchCnt()->qr2Port = 0;
#endif
    qr2_register_publicaddress_callback(DWCi_GetMatchCnt()->qr2Obj, DWCi_QR2PublicAddrCallback);
    qr2_register_natneg_callback(DWCi_GetMatchCnt()->qr2Obj, DWCi_QR2NatnegCallback);
    qr2_register_clientmessage_callback(DWCi_GetMatchCnt()->qr2Obj, DWCi_QR2ClientMsgCallback);
    qr2_send_statechanged(DWCi_GetMatchCnt()->qr2Obj);

    return qr2Error;
}
