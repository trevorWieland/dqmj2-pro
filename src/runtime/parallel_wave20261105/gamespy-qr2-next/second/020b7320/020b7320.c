#include "context.h"
void native_main_020b7320(qr2_t qrec, qr2_publicaddresscallback_t pacallback)
{
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_StackTrace,
		"qr2_register_publicaddress_callback()\r\n");
	if (qrec == NULL)
		qrec = native_data_020e179c;
	qrec->pa_callback = pacallback;
}
