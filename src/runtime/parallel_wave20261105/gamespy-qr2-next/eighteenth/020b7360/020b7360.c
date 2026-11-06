#include "context.h"
void native_main_020b7360(qr2_t qrec)
{
	struct sockaddr_in saddr;
	int error;
#if defined(_LINUX)
	unsigned int saddrlen = sizeof(struct sockaddr_in);
#else
	int saddrlen = sizeof(struct sockaddr_in);
#endif
	if (!qrec->read_socket)
		return;
	while(native_fn_020a8d88(qrec->hbsock))
	{
		error = (int)native_fn_020a8c00(qrec->hbsock, native_data_021d2f20, (INBUF_LEN - 1), 0, (struct sockaddr *)&saddr, &saddrlen);
		if (gsiSocketIsNotError(error))
		{
			native_data_021d2f20[error] = '\0';
			gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
				"Received %d bytes on query socket\r\n", error);
			gsDebugBinary(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_RawDump,
				native_data_021d2f20, error);
			native_fn_020b80a0(qrec, native_data_021d2f20, error, (struct sockaddr *)&saddr);
		}
		else if (error == 0)
		{
			gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
				"native_fn_020a8d88() returned true, but native_fn_020a8c00 return 0!\r\n", error);
		}
		else
		{
			gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
				"native_fn_020a8d88() returned true, but native_fn_020a8c00 failed!\r\n", error);
		}
	}
}
