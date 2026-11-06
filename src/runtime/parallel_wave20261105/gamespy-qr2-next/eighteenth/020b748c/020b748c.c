#include "context.h"
void native_main_020b748c(qr2_t qrec)
{
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_StackTrace,
		"qr2_send_statechanged()\r\n");
	if (qrec == NULL)
		qrec = native_data_020e179c;
	if (!qrec->ispublic)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_Warning,
			"Requested send statechange for LAN game, discarding\r\n");
		return;
	}
	if (native_fn_020a8ef8() - qrec->lastheartbeat < MIN_STATECHANGED_HB_TIME)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_Notice,
			"Queing statechange for later send (too soon)\r\n");
		qrec->userstatechangerequested = 1;
		return;
	}
	native_fn_020b8380(qrec, 1);
	qrec->userstatechangerequested = 0;
}
