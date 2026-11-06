#include "context.h"
void native_main_020b73c0(qr2_t qrec)
{
	gsi_time tc = native_fn_020a8ef8();
	if (INVALID_SOCKET == qrec->hbsock)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"HBSock is invalid\r\n");
		return;
	}
	if (qrec->listed_state > 0 && tc - qrec->lastheartbeat > FIRST_HB_TIME)
	{
		if (qrec->listed_state >= MAX_FIRST_COUNT)
		{
			gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_HotError,
				"No response from master, generating NoChallengeResponse error\r\n");
			qrec->listed_state = 0;
#ifndef GSI_UNICODE
			qrec->adderror_callback(e_qrnochallengeerror, native_data_020e2554, qrec->udata);
#else
			qrec->adderror_callback(e_qrnochallengeerror, Lnative_data_020e2554, qrec->udata);
#endif
			return;
		} else
		{
			native_fn_020b8380(qrec, 3);
			qrec->listed_state++;
		}
	}
	else if (qrec->userstatechangerequested && (tc - qrec->lastheartbeat > MIN_STATECHANGED_HB_TIME))
		native_fn_020b8380(qrec,1);
	else if (tc - qrec->lastheartbeat > HB_TIME || qrec->lastheartbeat == 0 || tc < qrec->lastheartbeat)
		native_fn_020b8380(qrec,0);
	if (native_fn_020a8ef8() - qrec->lastka > KA_TIME)
		native_fn_020b8334(qrec);
}
