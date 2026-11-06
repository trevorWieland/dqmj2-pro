#include "context.h"
void native_main_020b74d4(qr2_t qrec)
{
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_StackTrace,
		"qr2_shutdown()\r\n");
	if (qrec == NULL)
		qrec = native_data_020e179c;
	if (qrec->ispublic)
		native_fn_020b8380(qrec, 2);
	if (INVALID_SOCKET != qrec->hbsock && qrec->read_socket)
	{
		native_fn_020a8b6c(qrec->hbsock);
	}
	qrec->hbsock = INVALID_SOCKET;
	qrec->lastheartbeat = 0;
	if(qrec->read_socket)
	{
		native_fn_020a8ef4();
	}
	if (qrec != &native_data_020e17a0)
	{
		native_fn_020a929c(qrec);
	}
}
