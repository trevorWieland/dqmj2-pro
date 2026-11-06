#include "context.h"
void native_main_020a5d1c(SBQueryEngine *engine, SBBool icmpSocket)
{
	int i;
	char indata[MAX_RECVFROM_SIZE]; 
	struct sockaddr_in saddr;
	int saddrlen = sizeof(saddr);
	SBServer server;
	SOCKET recvSock = 0;

	if (icmpSocket)
	{
		#ifdef SB_ICMP_SUPPORT
			#if defined(SN_SYSTEMS) 
				ProcessIncomingICMPReplies(engine);
				return;
			#else
				recvSock = engine->icmpsock;
			#endif
		#endif
	}
	else
	{
		recvSock = engine->querysock;
	}
	
	
	while(CanReceiveOnSocket(recvSock))
	{
		i = (int)recvfrom(recvSock, indata, sizeof(indata) - 1, 0, (struct sockaddr *)&saddr, &saddrlen);

		if (gsiSocketIsError(i))
			break;
		indata[i] = 0;
		
		for (server = engine->querylist.first ; server != NULL ; server = server->next)
		{
			if ((icmpSocket && (server->flags & ICMP_IP_FLAG) && server->icmpip == saddr.sin_addr.s_addr) || 
				(server->publicip == saddr.sin_addr.s_addr && (server->publicport == saddr.sin_port || icmpSocket)) || 
				(server->publicip == engine->mypublicip && (server->flags & PRIVATE_IP_FLAG) && server->privateip == saddr.sin_addr.s_addr && server->privateport == saddr.sin_port)) 
			{
				if (icmpSocket)
				{
					if (ParseSingleICMPReply(engine, server, indata, i))
						break; 
				} else
				{
					if (engine->queryversion == QVERSION_QR2)
						ParseSingleQR2Reply(engine, server, indata, i);
					else
						ParseSingleGOAReply(engine, server, indata, i);
					break;
				}
			}
		}		
	}


}