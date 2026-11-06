#include "context.h"
void native_main_020b78ac(qr2_t qrec, char * buffer)
{
	unsigned int ip;
	unsigned int portTemp;
	unsigned short port;
	native_fn_02019dd4(buffer, native_data_020e25a0, &ip, &portTemp);
	port = (unsigned short)portTemp;
	ip = htonl(ip);
	if((ip == 0) || (port == 0))
		return;
#ifdef GSI_COMMON_DEBUG
	{
		IN_ADDR addr;
		addr.s_addr = ip;
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Received public address (%s:%d)\r\n", inet_ntoa(addr), port);
	}
#endif
	if((qrec->publicip != ip) || (qrec->publicport != port))
	{
		qrec->publicip = ip;
		qrec->publicport = port;
		qrec->pa_callback(ip, port, qrec->udata);
	}
}
