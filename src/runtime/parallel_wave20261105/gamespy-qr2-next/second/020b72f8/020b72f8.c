#include "context.h"
void native_main_020b72f8(qr2_t qrec, qr2_natnegcallback_t nncallback)
{
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_StackTrace,
		"qr2_register_natneg_callback()\r\n");
	if (qrec == NULL)
		qrec = native_data_020e179c;
	qrec->nn_callback = nncallback;
}
