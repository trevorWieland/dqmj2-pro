#include "context.h"
GPResult
native_main_020affbc(
  GPConnection * connection,
  GPIPeer * peer
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	
	GSUdpPeerState aPeerState;
	GPIBool connClosed;
	GPICallback callback;
	char * buffer;
	int type;
	int messageLen;
	GPResult result;

	GS_ASSERT(peer);
	if (!peer)
		return GP_NETWORK_ERROR;
	
	
	if(peer->outputBuffer.len)
	{
		
		result = gpiSendBufferToPeer(connection, peer->ip, peer->port, &peer->outputBuffer, &connClosed, GPITrue);
		if(connClosed || (result != GP_NO_ERROR))
		{
			peer->state = GPI_PEER_DISCONNECTED;
			return GP_NO_ERROR;
		}
	}

	
	
	if(!peer->outputBuffer.len)
	{
		CHECK_RESULT(gpiPeerSendMessages(connection, peer));
		if(peer->state == GPI_PEER_DISCONNECTED)
			return GP_NO_ERROR;
	}

	
	
	
	if(peer->inputBuffer.len > 0)
	{
		peer->timeout = (time(NULL) + GPI_PEER_TIMEOUT);
	}

	
	
	do
	{
		
		
		CHECK_RESULT(gpiReadMessageFromBuffer(connection, &peer->inputBuffer, &buffer, &type, &messageLen));
		if(buffer != NULL)
		{
			
			
			switch(type)
			{
			case GPI_BM_MESSAGE:
				callback = iconnection->callbacks[GPI_RECV_BUDDY_MESSAGE];
				if(callback.callback != NULL)
				{
					GPRecvBuddyMessageArg * arg;

					arg = (GPRecvBuddyMessageArg *)gsimalloc(sizeof(GPRecvBuddyMessageArg));
					if(arg == NULL)
						Error(connection, GP_MEMORY_ERROR, native_data_020e104c);
					arg->profile = peer->profile;
#ifndef GSI_UNICODE
					arg->message = goastrdup(buffer);
#else
					arg->message = UTF8ToUCS2StringAlloc(buffer);
#endif
					arg->date = (unsigned int)time(NULL);
					CHECK_RESULT(gpiAddCallback(connection, callback, arg, NULL, GPI_ADD_MESSAGE));
				}
				break;
				
			case GPI_BM_UTM:
				callback = iconnection->callbacks[GPI_RECV_BUDDY_UTM];
				if (callback.callback != NULL)
				{
					GPRecvBuddyUTMArg * arg;

					arg = (GPRecvBuddyUTMArg *)gsimalloc(sizeof(GPRecvBuddyUTMArg));
					if(arg == NULL)
						Error(connection, GP_MEMORY_ERROR, native_data_020e104c);
					arg->profile = peer->profile;
#ifndef GSI_UNICODE
					arg->message = goastrdup(buffer);
#else
					arg->message = UTF8ToUCS2StringAlloc(buffer);
#endif
					arg->date = (unsigned int)time(NULL);
					CHECK_RESULT(gpiAddCallback(connection, callback, arg, NULL, GPI_ADD_MESSAGE));
				}
				break;

			case GPI_BM_PING:
				
				
				gpiSendBuddyMessage(connection, peer->profile, GPI_BM_PONG, native_data_020e105c, 0, NULL);

				break;

#ifndef NOFILE
			case GPI_BM_PONG:
				
				
				gpiTransfersHandlePong(connection, peer->profile, peer);
				break;
#endif
			case GPI_BM_KEYS_REQUEST:
				CHECK_RESULT(gpiBuddyHandleKeyRequest(connection, peer));
				break;
			case GPI_BM_KEYS_REPLY:
				CHECK_RESULT(gpiBuddyHandleKeyReply(connection, peer, buffer));
				
				
				break;
			case GPI_BM_FILE_SEND_REQUEST:
			case GPI_BM_FILE_SEND_REPLY:
			case GPI_BM_FILE_BEGIN:
			case GPI_BM_FILE_END:
			case GPI_BM_FILE_DATA:
			case GPI_BM_FILE_SKIP:
			case GPI_BM_FILE_TRANSFER_THROTTLE:
			case GPI_BM_FILE_TRANSFER_CANCEL:
			case GPI_BM_FILE_TRANSFER_KEEPALIVE:
				
				
				gpiHandleTransferMessage(connection, peer, type, peer->inputBuffer.buffer, buffer, messageLen);


				break;

			default:
				break;
			}

			
			
			gpiClipBufferToPosition(connection, &peer->inputBuffer);
		}
	}
	while(buffer);

	gsUdpEngineGetPeerState(peer->ip, peer->port, &aPeerState);
	
	if (aPeerState == GS_UDP_PEER_CLOSED)
		peer->state = GPI_PEER_DISCONNECTED;
	
	return GP_NO_ERROR;
}