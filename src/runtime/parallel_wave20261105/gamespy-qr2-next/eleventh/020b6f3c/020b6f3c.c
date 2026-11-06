#include "context.h"
void native_main_020b6f3c(NATNegotiator neg, NatNegPacket *p, struct sockaddr_in *fromaddr)
{
	gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
		"Got connect packet (finish code: %d), guess: %s:%d\n", p->Packet.Connect.finished, inet_ntoa(*(struct in_addr *)&p->Packet.Connect.remoteIP), ntohs(p->Packet.Connect.remotePort));
	if (p->Packet.Connect.finished == FINISHED_NOERROR)
		native_fn_020b6eac(neg, fromaddr);
	if (neg->state >= ns_connectping)
		return;
	if (p->Packet.Connect.finished != FINISHED_NOERROR)
	{
		NegotiateResult errcode;
		errcode = nr_unknownerror;
		if (p->Packet.Connect.finished == FINISHED_ERROR_DEADBEAT_PARTNER)
			errcode = nr_deadbeatpartner;
		else if (p->Packet.Connect.finished == FINISHED_ERROR_INIT_PACKETS_TIMEDOUT)
			errcode = nr_inittimeout;
		native_fn_020b67e0(neg, errcode, INVALID_SOCKET, NULL);
		return;
	}
	neg->guessedIP = p->Packet.Connect.remoteIP;
	neg->guessedPort = ntohs(p->Packet.Connect.remotePort);
	neg->retryCount = 0;
	neg->state = ns_connectping;
	neg->progressCallback(neg->state, neg->userdata);
	native_fn_020b69e4(neg);
}
