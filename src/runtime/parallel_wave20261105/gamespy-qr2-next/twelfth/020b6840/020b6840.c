#include "context.h"
void native_main_020b6840(NATNegotiator neg)
{
	char buffer[INITPACKET_SIZE + sizeof(native_data_021d23f0)];
	NatNegPacket * p = (NatNegPacket *)buffer;
	unsigned int localip;
	unsigned short localport;
	int packetlen;
	memcpy(p->magic, native_data_020e1738, NATNEG_MAGIC_LEN);
	p->version = NN_PROTVER;
	p->packettype = NN_INIT;
	p->cookie = (int)htonl((unsigned int)neg->cookie);
	p->Packet.Init.clientindex = (unsigned char)neg->clientindex;
	p->Packet.Init.usegameport = (unsigned char)((neg->gameSock == INVALID_SOCKET) ? 0 : 1);
	localip = ntohl(native_fn_020b66a4());
	buffer[INITPACKET_ADDRESS_OFFSET] = (char)((localip >> 24) & 0xFF);
	buffer[INITPACKET_ADDRESS_OFFSET+1] = (char)((localip >> 16) & 0xFF);
	buffer[INITPACKET_ADDRESS_OFFSET+2] = (char)((localip >> 8) & 0xFF);
	buffer[INITPACKET_ADDRESS_OFFSET+3] = (char)(localip & 0xFF);
	buffer[INITPACKET_ADDRESS_OFFSET+4] = 0;
	buffer[INITPACKET_ADDRESS_OFFSET+5] = 0;
	native_fn_0201d6b8(buffer + INITPACKET_SIZE, native_data_021d23f0);
	packetlen = (INITPACKET_SIZE + (int)native_fn_0201d69c(native_data_021d23f0) + 1);
	if (p->Packet.Init.usegameport && !neg->initAckRecv[NN_PT_GP])
	{
		p->Packet.Init.porttype = NN_PT_GP;
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Sending INIT (GP) to %s:%d...\n", inet_ntoa(*(struct in_addr *)&matchup1ip), MATCHUP_PORT1);
		native_fn_020b6670(neg->gameSock, matchup1ip, MATCHUP_PORT1, p, packetlen);
	}
	if (!neg->initAckRecv[NN_PT_NN1])
	{
		p->Packet.Init.porttype = NN_PT_NN1;
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Sending INIT (NN1) to %s:%d...\n", inet_ntoa(*(struct in_addr *)&matchup1ip), MATCHUP_PORT1);
		native_fn_020b6670(neg->negotiateSock, matchup1ip, MATCHUP_PORT1, p, packetlen);
	}
	localport = ntohs(native_fn_020b66e0((p->Packet.Init.usegameport) ?  neg->gameSock : neg->negotiateSock));
	buffer[INITPACKET_ADDRESS_OFFSET+4] = (char)((localport >> 8) & 0xFF);
	buffer[INITPACKET_ADDRESS_OFFSET+5] = (char)(localport & 0xFF);
	if (!neg->initAckRecv[NN_PT_NN2])
	{
		p->Packet.Init.porttype = NN_PT_NN2;
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Sending INIT (NN2) to %s:%d...\n", inet_ntoa(*(struct in_addr *)&matchup2ip), MATCHUP_PORT2);
		native_fn_020b6670(neg->negotiateSock, matchup2ip, MATCHUP_PORT2, p, packetlen);
	}
	if (!neg->initAckRecv[NN_PT_NN3])
	{
		p->Packet.Init.porttype = NN_PT_NN3;
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Sending INIT (NN3) to %s:%d...\n", inet_ntoa(*(struct in_addr *)&matchup3ip), MATCHUP_PORT3);
		native_fn_020b6670(neg->negotiateSock, matchup3ip, MATCHUP_PORT3, p, packetlen);
	}
	neg->retryTime = native_fn_020a8ef8() + INIT_RETRY_TIME;
	neg->maxRetryCount = INIT_RETRY_COUNT;
}
