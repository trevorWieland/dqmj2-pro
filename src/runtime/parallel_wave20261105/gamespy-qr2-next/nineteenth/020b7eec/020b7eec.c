#include "context.h"
gsi_bool native_main_020b7eec(qr2_t qrec, struct qr2_buffer_s* buf, struct sockaddr_in* sender)
{
	int i=0;
	gsi_time now = native_fn_020a8ef8();
	int firstFreeIndex = -1;
	int numDuplicates = 0;
	if ((qrec->backendoptions & QR2_OPTION_USE_QUERY_CHALLENGE) == 0)
	{
		native_fn_020b7568(buf, 0);
		return gsi_true;
	}
	for (; i < QR2_IPVERIFY_ARRAY_SIZE; i++)
	{
		if (firstFreeIndex == -1 && qrec->ipverify[i].addr.sin_addr.s_addr == 0)
			firstFreeIndex = i;
		if (qrec->ipverify[i].addr.sin_addr.s_addr == sender->sin_addr.s_addr &&
			qrec->ipverify[i].addr.sin_port == sender->sin_port)
		{
			numDuplicates++;
		}
	}
	if (numDuplicates > QR2_IPVERIFY_MAXDUPLICATES)
		return gsi_false;
	if (firstFreeIndex == -1)
		return gsi_false;
	qrec->ipverify[firstFreeIndex].addr = *sender;
	qrec->ipverify[firstFreeIndex].challenge = htonl( (native_fn_0201d5d4() << 16) | native_fn_0201d5d4() );
	qrec->ipverify[firstFreeIndex].createtime = now;
	native_fn_020b7568(buf, (int)qrec->ipverify[firstFreeIndex].challenge);
	return gsi_true;
}
