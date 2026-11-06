#include "context.h"
gsi_bool native_main_020b8010(qr2_t qrec, struct sockaddr_in* sender, gsi_u32 ipverify)
{
	int i=0;
	for (; i < QR2_IPVERIFY_ARRAY_SIZE; i++)
	{
		if (qrec->ipverify[i].addr.sin_addr.s_addr == sender->sin_addr.s_addr &&
			qrec->ipverify[i].addr.sin_port == sender->sin_port)
		{
			if (qrec->ipverify[i].challenge == ipverify)
			{
				qrec->ipverify[i].addr.sin_addr.s_addr = 0;
				qrec->ipverify[i].addr.sin_port = 0;
				return gsi_true;
			}
		}
	}
	return gsi_false;
}
