#include "context.h"
void native_main_020b6eac(NATNegotiator neg, struct sockaddr_in *toaddr)
{
	NatNegPacket p;
	memcpy(p.magic, native_data_020e1738, NATNEG_MAGIC_LEN);
	p.version = NN_PROTVER;
	p.packettype = NN_CONNECT_ACK;
	p.cookie = (int)htonl((unsigned int)neg->cookie);
	p.Packet.Init.clientindex = (unsigned char)neg->clientindex;
	gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
		"Sending connect ack...\n");
	native_fn_020b6670(neg->negotiateSock, toaddr->sin_addr.s_addr, ntohs(toaddr->sin_port), &p, INITPACKET_SIZE);
}
