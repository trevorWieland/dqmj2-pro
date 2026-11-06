#include "context.h"
void native_main_020a58dc(SBQueryEngine *engine, SBServer server)
{
	unsigned char queryBuffer[256];
	int queryLen;
	gsi_bool querySuccess = gsi_false;
	struct sockaddr_in saddr;

	saddr.sin_family = AF_INET;
	server->updatetime = current_time();

	if (server->state & STATE_PENDINGICMPQUERY) 
	{
#ifdef SB_ICMP_SUPPORT
	#if !defined(SN_SYSTEMS)
		SBICMPHeader *_icmp = (SBICMPHeader *)(queryBuffer);
		
		_icmp->type = SB_ICMP_ECHO;
		_icmp->code = 0;
		_icmp->un.idseq = server->updatetime; 
		_icmp->cksum = 0;
		queryLen = sizeof(SBICMPHeader) + 6;
		memcpy(queryBuffer + sizeof(SBICMPHeader), &server->publicip, 4); 
		memcpy(queryBuffer + sizeof(SBICMPHeader) + 4, &server->publicport, 2); 
		_icmp->cksum = IPChecksum((unsigned short *)queryBuffer, queryLen);
		if (SBServerGetFlags(server) & ICMP_IP_FLAG) 
		{
			saddr.sin_addr.s_addr = server->icmpip;
		} else
		{
			saddr.sin_addr.s_addr = server->publicip;
		}

		sendto(engine->icmpsock, (char *)queryBuffer, queryLen, 0, (struct sockaddr *)&saddr, sizeof(saddr));
		querySuccess = gsi_true;
	#else
		int result;
		sndev_set_ping_ip_type optval;
		optval.ip_addr = server->icmpip;

		gsDebugFormat(GSIDebugCat_SB, GSIDebugType_Network, GSIDebugLevel_WarmError,
				"Attempting to send ICMP ping to %s\r\n", inet_ntoa(*((struct in_addr*)&server->icmpip)));

		result = sndev_set_options(0, SN_DEV_SET_PING_IP, (void*)&optval, sizeof(optval)); 
		if (result==SN_PING_FAIL)
		{
			gsDebugFormat(GSIDebugCat_SB, GSIDebugType_Network, GSIDebugLevel_WarmError,
				"ICMP ping attempt failed on SNSystems (unknown error)\r\n");
			querySuccess = gsi_true; 
		}
		else if (result==SN_PING_FULL)
		{
			gsDebugFormat(GSIDebugCat_SB, GSIDebugType_Network, GSIDebugLevel_WarmError,
				"ICMP ping attempt failed on SNSystems (SN_PING_FULL)\r\n");
			querySuccess = gsi_false;
		}
		else
			querySuccess = gsi_true;
	#endif
#endif
	} else 
	{
		if (engine->queryversion == QVERSION_QR2)
		{
			if (server->state & STATE_PENDINGQUERYCHALLENGE)
			{
				
				int pos = 0;
				queryBuffer[pos++] = QR2_MAGIC_1;
				queryBuffer[pos++] = QR2_MAGIC_2;
				queryBuffer[pos++] = 0x09; 
				
				memcpy(&queryBuffer[pos], &server->updatetime, 4);
				pos += 4;
				queryLen = pos;
			}
			else
			{
				volatile gsi_u32 challengeNBO = htonl(server->querychallenge);
				int pos = 0;

				
				queryBuffer[pos++] = QR2_MAGIC_1;
				queryBuffer[pos++] = QR2_MAGIC_2;
				queryBuffer[pos++] = 0;
				memcpy(&queryBuffer[pos], &server->updatetime, 4); 
				pos += 4;
				if (challengeNBO != 0)
				{
					memcpy(&queryBuffer[pos], &challengeNBO, 4); 
					pos += 4;
				}
				if (server->state & STATE_PENDINGBASICQUERY) 
				{
					int i;
					queryBuffer[pos++] = (unsigned char)engine->numserverkeys;
					for (i = 0 ; i < engine->numserverkeys ; i++)
						queryBuffer[pos++] = engine->serverkeys[i];

					
					queryBuffer[pos++] = 0x00;
					queryBuffer[pos++] = 0x00;
					queryLen = pos;

				} else  
				{
					queryBuffer[pos++] = 0xFF;
					queryBuffer[pos++] = 0xFF;
					queryBuffer[pos++] = 0xFF;
					
					
					queryBuffer[pos++] = 0x1;
					queryLen = pos; 
				}
			}
		} else 
		{
			if (server->state & STATE_PENDINGBASICQUERY) 
			{
				memcpy(queryBuffer, BASIC_GOA_QUERY, BASIC_GOA_QUERY_LEN);
				queryLen = BASIC_GOA_QUERY_LEN;
			} else 
			{
				memcpy(queryBuffer, FULL_GOA_QUERY, FULL_GOA_QUERY_LEN);
				queryLen = FULL_GOA_QUERY_LEN;		
			}
		}
		if (server->publicip == engine->mypublicip && (server->flags & PRIVATE_IP_FLAG)) 
		{
			saddr.sin_addr.s_addr = server->privateip;
			saddr.sin_port = server->privateport;
		} else
		{
			saddr.sin_addr.s_addr = server->publicip;
			saddr.sin_port = server->publicport;
		}
		sendto(engine->querysock, (char *)queryBuffer, queryLen, 0, (struct sockaddr *)&saddr, sizeof(saddr));
		querySuccess = gsi_true;
	}

	
	if (querySuccess)
		FIFOAddRear(&engine->querylist, server);
	else
		server->updatetime = 0;
}