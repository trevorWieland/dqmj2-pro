#include "context.h"
GPResult
native_main_020afbc8(
  GPConnection * connection,
  GPIPeer * peer
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	
	char * str = NULL;
	
	GPIBool connClosed;
	GPIProfile * pProfile;
	GPResult result;
	GSUdpPeerState aPeerState;
	
	GS_ASSERT(peer);
	if (!peer)
		return GP_NETWORK_ERROR;

	GS_ASSERT(peer->state != GPI_PEER_DISCONNECTED && peer->state != GPI_PEER_NOT_CONNECTED);
	if (peer->state == GPI_PEER_DISCONNECTED || peer->state == GPI_PEER_NOT_CONNECTED)
		return GP_NETWORK_ERROR;
	
	
	switch(peer->state)
	{
		case GPI_PEER_GETTING_SIG:
			
			
			break;

		case GPI_PEER_GOT_SIG:
		{
			
			
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_State, GSIDebugLevel_Verbose, "Got the peer signature for profileid: %d\n", peer->profile);
			CHECK_RESULT(gpiPeerStartConnect(connection, peer));

			break;
		}
		case GPI_PEER_CONNECTING:
		{	
			
			
			

			gsUdpEngineGetPeerState(peer->ip, peer->port, &aPeerState);

			if(aPeerState == GS_UDP_PEER_CONNECTED)
			{
				GPIPeer * pcurr;
				GPIBool freePeerSig = GPITrue;

				
				
				if(!gpiGetProfile(connection, peer->profile, &pProfile))
					Error(connection, GP_NETWORK_ERROR, native_data_020e0fac);

				
				
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, native_data_020e0fc8);
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, native_data_020e0fd0);
				gpiAppendIntToBuffer(connection, &peer->outputBuffer, iconnection->profileid);
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, native_data_020e0fd8);
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, iconnection->nick);
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, native_data_020e0fe0);
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, pProfile->peerSig);
				gpiAppendStringToBuffer(connection, &peer->outputBuffer, native_data_020e0fe8);

				
				
				for(pcurr = iconnection->peerList ; pcurr != NULL ; pcurr = pcurr->pnext)
					if((pcurr->profile == peer->profile) && (pcurr != peer))
						if(pcurr->state <= GPI_PEER_CONNECTING)
							freePeerSig = GPIFalse;

				
				
				if(freePeerSig)
				{
					freeclear(pProfile->peerSig);
					if(gpiCanFreeProfile(pProfile))
						gpiRemoveProfile(connection, pProfile);
				}

				
				
				peer->state = GPI_PEER_WAITING;
			}
			
			break;
		}
		case GPI_PEER_WAITING:
		{
			
			
			

			
			
			if (peer->inputBuffer.buffer)
				str = strstr(peer->inputBuffer.buffer, native_data_020e0fe8);
			if(str != NULL)
			{
				str[0] = '\0';
				str += 7;

				
				
				if(strncmp(peer->inputBuffer.buffer, native_data_020e0ff0, 7) == 0)
				{
					
					
					peer->nackCount++;

					
					
					if(peer->nackCount > 1)
					{
						
						

						
						
						Error(connection, GP_NETWORK_ERROR, native_data_020e0ff8);
					}

					
					
					CHECK_RESULT(gpiPeerGetSig(connection, peer));
				}
				else if(strncmp(peer->inputBuffer.buffer, native_data_020e101c, 6) != 0)
				{
					
					
					Error(connection, GP_NETWORK_ERROR, native_data_020e1024);
				}

				
				
				peer->state = GPI_PEER_CONNECTED;
				peer->inputBuffer.len = 0;
			}

			break;
		}
		
		default: break;
	}

	
	
	if(peer->outputBuffer.len > 0)
	{
		
		result = gpiSendBufferToPeer(connection, peer->ip, peer->port, &peer->outputBuffer, &connClosed, GPITrue);
		if(connClosed || (result != GP_NO_ERROR))
			peer->state = GPI_PEER_DISCONNECTED;
	}
	
	return GP_NO_ERROR;
}