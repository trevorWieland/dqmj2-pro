#include "context.h"
GPResult
native_main_020aff44(
  GPConnection * connection,
  GPIPeer * peer
)
{
	GPIBool connClosed;
	GPIMessage * message;
	GPResult result;

	GS_ASSERT(peer);
	if (!peer)
		return GP_NETWORK_ERROR;
	
	
	if(peer->outputBuffer.len)
		return GP_NO_ERROR;

	
	
	while(ArrayLength(peer->messages))
	{
		
		
		message = (GPIMessage *)ArrayNth(peer->messages, 0);

		
		
		
		result = gpiSendBufferToPeer(connection, peer->ip, peer->port, &message->buffer, &connClosed, GPIFalse);
		if(connClosed || (result != GP_NO_ERROR))
		{
			peer->state = GPI_PEER_DISCONNECTED;
			return GP_NO_ERROR;
		}

		
		
		if(message->buffer.pos != message->buffer.len)
			break;

		
		
		ArrayDeleteAt(peer->messages, 0);
	}

	return GP_NO_ERROR;
}