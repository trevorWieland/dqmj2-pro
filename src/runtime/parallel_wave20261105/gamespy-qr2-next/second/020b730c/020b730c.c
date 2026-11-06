#include "context.h"
void native_main_020b730c(qr2_t qrec, qr2_clientmessagecallback_t cmcallback)
{
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_StackTrace,
		"qr2_register_clientmessage_callback()\r\n");
	if (qrec == NULL)
		qrec = native_data_020e179c;
	qrec->cm_callback = cmcallback;
}
