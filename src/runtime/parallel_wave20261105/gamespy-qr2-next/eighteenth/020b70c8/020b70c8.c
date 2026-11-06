#include "context.h"
void native_main_020b70c8(char *data, int len, struct sockaddr_in *fromaddr)
{
	NatNegPacket p;
	NATNegotiator neg;
	unsigned char ptype;
	if (!native_fn_020b6654(data))
		return;
	ptype = *(unsigned char *)(data + offsetof(NatNegPacket, packettype));
	gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
		"Process data, packet type: %d, %d bytes (%s:%d)\n", ptype, len, inet_ntoa(fromaddr->sin_addr), ntohs(fromaddr->sin_port));
	if (ptype == NN_CONNECT || ptype == NN_CONNECT_PING)
	{
		if (len < CONNECTPACKET_SIZE)
			return;
		copy20(&p,data);
		neg = native_fn_020b6564((int)ntohl((unsigned int)p.cookie));
		if (neg)
		{
			if (ptype == NN_CONNECT)
				native_fn_020b6f3c(neg, &p, fromaddr);
			else
				native_fn_020b6fa8(neg, &p, fromaddr);
		}
	} else
	{
		if (len < INITPACKET_SIZE)
			return;
		copy21(&p,data);
		neg = native_fn_020b6564((int)ntohl((unsigned int)p.cookie));
		if (neg)
			native_fn_020b7014(neg, &p, fromaddr);
	}
}
