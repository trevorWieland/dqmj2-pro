#include "context.h"
void native_main_020b8334(qr2_t qrec)
{
	struct qr2_buffer_s buf;
	buf.len = 0;
	native_fn_020b7828(&buf, PACKET_KEEPALIVE, qrec->instance_key);
	native_fn_020a8c34(qrec->hbsock, buf.buffer, buf.len, 0, (struct sockaddr *)&(qrec->hbaddr), sizeof(struct sockaddr_in));
	qrec->lastka = native_fn_020a8ef8();
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
		"Sent keepalive to master\r\n", buf);
}
