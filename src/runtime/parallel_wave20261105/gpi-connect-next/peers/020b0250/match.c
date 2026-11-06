#include "context.h"
GPResult
native_main_020b0250(
  GPConnection * connection,
  GPIPeer * peer
)
{
	GPResult result = GP_NO_ERROR;
	
	
	
	GS_ASSERT(peer->state != GPI_PEER_NOT_CONNECTED);
	if (peer->state == GPI_PEER_NOT_CONNECTED)
		return GP_NETWORK_ERROR;

	
	
	if(peer->state != GPI_PEER_CONNECTED)
	{
		if(peer->initiated)
			result = gpiProcessPeerInitiatingConnection(connection, peer);
		else
			result = gpiProcessPeerAcceptingConnection(connection, peer);
	}

	
	
	if((result == GP_NO_ERROR) && (peer->state == GPI_PEER_CONNECTED))
	{
		result = gpiProcessPeerConnected(connection, peer);
		gpiCheckTimedOutPeerOperations(connection, peer);
	}

	return result;
}