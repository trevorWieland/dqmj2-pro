#include "context.h"
void native_main_020b8380(qr2_t qrec, int statechanged)
{
	struct qr2_buffer_s buf;
	int i;
	char ipkey[20];
	buf.len = 0;
	native_fn_020b7828(&buf, PACKET_HEARTBEAT, qrec->instance_key);
	for (i = 0 ; i < native_data_021d2ec8 ; i++)
	{
		native_fn_0200616c(ipkey, native_data_020e25cc, i);
		native_fn_020b7588(&buf, ipkey);
		native_fn_020b7588(&buf, native_fn_0209073c(native_data_021d2ecc[i]));
	}
	native_fn_020b7588(&buf, native_data_020e25d8);
	native_fn_020b7568(&buf, qrec->qport);
	native_fn_020b7588(&buf, native_data_020e25e4);
	native_fn_020b7588(&buf, qrec->nat_negotiate ? native_data_020e25ec : native_data_020e25f0);
	if(statechanged)
	{
		native_fn_020b7588(&buf, native_data_020e25f4);
		native_fn_020b7568(&buf, statechanged);
	}
	native_fn_020b7588(&buf, native_data_020e2604);
	native_fn_020b7588(&buf, qrec->gamename);
	if(qrec->pa_callback)
	{
		native_fn_020b7588(&buf, native_data_020e2610);
		native_fn_020b7568(&buf, (int)qrec->publicip);
		native_fn_020b7588(&buf, native_data_020e261c);
		native_fn_020b7568(&buf, qrec->publicport);
	}
	if (statechanged != 2)
	{
		struct qr2_buffer_s temp;
		native_fn_0201b19c(temp.buffer, buf.buffer, (size_t)buf.len);
		temp.len = buf.len;
		native_fn_020b7ac8(qrec, &temp, 0xFF, NULL, 0xFF, NULL, 0xFF, NULL);
		if(AVAILABLE_BUFFER_LEN(&temp) < 1)
		{
			temp.len = buf.len;
			native_fn_020b7ac8(qrec, &temp, 0xFF, NULL, 0, NULL, 0, NULL);
		}
		native_fn_0201b19c(buf.buffer, temp.buffer, (size_t)temp.len);
		buf.len = temp.len;
	}
	else
	{
		if (AVAILABLE_BUFFER_LEN(&buf) >= 1)
			buf.buffer[buf.len++] = 0;
	}
	native_fn_020a8c34(qrec->hbsock, buf.buffer, buf.len, 0, (struct sockaddr *)&(qrec->hbaddr), sizeof(struct sockaddr_in));
	qrec->lastka = qrec->lastheartbeat = native_fn_020a8ef8();
	if (statechanged != 0)
		qrec->userstatechangerequested = 0;
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
		"Sent heartbeat to master (size %d)\r\n", buf.len);
	gsDebugBinary(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_RawDump,
		buf.buffer, buf.len);
}
