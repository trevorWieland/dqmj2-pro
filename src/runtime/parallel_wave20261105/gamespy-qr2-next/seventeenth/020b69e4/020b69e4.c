#include "context.h"
void native_main_020b69e4(NATNegotiator neg)
{
	NatNegPacket p;
	memcpy(p.magic, native_data_020e1738, NATNEG_MAGIC_LEN);
	p.version = NN_PROTVER;
	p.packettype = NN_CONNECT_PING;
	p.cookie = (int)htonl((unsigned int)neg->cookie);
	p.Packet.Connect.remoteIP = neg->guessedIP;
	p.Packet.Connect.remotePort = htons(neg->guessedPort);
	p.Packet.Connect.gotyourdata = neg->gotRemoteData;
	p.Packet.Connect.finished = (unsigned char)((neg->state == ns_connectping) ? 0 : 1);
	gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
		"Sending PING to %s:%d (got remote data: %d)\n", inet_ntoa(*(struct in_addr *)&neg->guessedIP), neg->guessedPort,   neg->gotRemoteData);
	native_fn_020b6670((neg->gameSock != INVALID_SOCKET) ? neg->gameSock : neg->negotiateSock, neg->guessedIP, neg->guessedPort,  &p, CONNECTPACKET_SIZE);
	neg->retryTime = native_fn_020a8ef8() + PING_RETRY_TIME;
	neg->maxRetryCount = PING_RETRY_COUNT;
	if(neg->gotRemoteData)
		neg->sendGotRemoteData = 1;
}
