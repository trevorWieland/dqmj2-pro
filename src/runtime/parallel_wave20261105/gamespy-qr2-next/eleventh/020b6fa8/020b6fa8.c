#include "context.h"
void native_main_020b6fa8(NATNegotiator neg, NatNegPacket *p, struct sockaddr_in *fromaddr)
{
	if (neg->state < ns_connectping)
		return;
	gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
		"Got ping from: %s:%d (gotmydata: %d, finished: %d)\n", inet_ntoa(fromaddr->sin_addr), ntohs(fromaddr->sin_port), p->Packet.Connect.gotyourdata, p->Packet.Connect.finished);
	neg->guessedIP = fromaddr->sin_addr.s_addr;
	neg->guessedPort = ntohs(fromaddr->sin_port);
	neg->gotRemoteData = 1;
	if (!p->Packet.Connect.gotyourdata)
		native_fn_020b69e4(neg);
	else
	{
		if (neg->state == ns_connectping)
		{
			gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
				"CONNECT FINISHED\n");
			if(!neg->sendGotRemoteData)
				native_fn_020b69e4(neg);
			neg->state = ns_finished;
			neg->retryTime = native_fn_020a8ef8() + FINISHED_IDLE_TIME;
		} else if (!p->Packet.Connect.finished)
			native_fn_020b69e4(neg);
	}
}
