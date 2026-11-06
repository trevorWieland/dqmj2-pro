#include "context.h"
void native_main_020b7014(NATNegotiator neg, NatNegPacket *p, struct sockaddr_in *fromaddr)
{
	switch (p->packettype)
	{
	case NN_INITACK:
		if (p->Packet.Init.porttype > NN_PT_NN3)
			return;
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Got init ack for port %d\n", p->Packet.Init.porttype);
		neg->initAckRecv[p->Packet.Init.porttype] = 1;
		if (neg->state == ns_initsent)
		{
			if (neg->initAckRecv[NN_PT_NN1] != 0 && neg->initAckRecv[NN_PT_NN2] != 0 && neg->initAckRecv[NN_PT_NN3] != 0 &&
				(neg->gameSock == INVALID_SOCKET ||  neg->initAckRecv[NN_PT_GP] != 0))
			{
				neg->state = ns_initack;
				neg->retryTime = native_fn_020a8ef8() + PARTNER_WAIT_TIME;
				neg->progressCallback(neg->state, neg->userdata);
			}
		}
		break;
	case NN_ERTTEST:
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Got ERT\n");
		p->packettype = NN_ERTACK;
		native_fn_020b6670(neg->negotiateSock, fromaddr->sin_addr.s_addr, ntohs(fromaddr->sin_port), p, INITPACKET_SIZE);
		break;
	case NN_REPORT_ACK:
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Got REPORT ACK\n");
		neg->state = ns_reportack;
		neg->completedCallback(neg->result, neg->connectedSocket, (struct sockaddr_in *)&neg->remoteaddr, neg->userdata);
		if (neg->gameSock == INVALID_SOCKET)
			neg->negotiateSock = INVALID_SOCKET;
		native_fn_020b6c90(neg->cookie);
		break;
	}
}
