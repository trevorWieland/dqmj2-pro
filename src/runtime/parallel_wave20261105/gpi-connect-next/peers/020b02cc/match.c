#include "context.h"
void
native_main_020b02cc(
  GPConnection * connection,
  GPIPeer * peer
)
{
	GPIPeer * pprev;
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIMessage * message;

	GS_ASSERT(peer != NULL);
	if (peer == NULL)
		return;

	GS_ASSERT(iconnection->peerList);
	if (iconnection->peerList == NULL)
		return;
	
	
	if(iconnection->peerList == peer)
	{
		iconnection->peerList = peer->pnext;
	}
	else
	{
		
		
		for(pprev = iconnection->peerList ; pprev->pnext != peer ; pprev = pprev->pnext)
		{
			if(pprev->pnext == NULL)
			{
				
				
				assert(0);
				gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Misc, GSIDebugLevel_HotError,
					"Tried to remove peer not in list.");
				return;
			}
		}
		pprev->pnext = peer->pnext;
	}

	
	
	while(ArrayLength(peer->messages))
	{
		
		
		message = (GPIMessage *)ArrayNth(peer->messages, 0);

		
		
		if(message->type < 100)
			gpiSendServerBuddyMessage(connection, peer->profile, message->type, message->buffer.buffer + message->start);

		
		
		ArrayDeleteAt(peer->messages, 0);
	}

	gpiDestroyPeer(connection, peer);
}