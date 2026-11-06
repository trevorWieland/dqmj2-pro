#include "context.h"
void
native_main_020b01e0(GPConnection * connection, GPIPeer *peer)
{
	GPIPeerOp *anIterator = peer->peerOpQueue.first;
	GS_ASSERT(peer);
	if (!peer)
		return;
	
	while (anIterator && anIterator != peer->peerOpQueue.last)
	{
		if (anIterator->state != GPI_PEER_OP_STATE_FINISHED &&  current_time() > anIterator->timeout && anIterator->callback)
		{
			
			
			
			if (anIterator->type == GPI_BM_KEYS_REQUEST)
			{	
				GPICallback callback;
				GPGetBuddyStatusInfoKeysArg *arg = (GPGetBuddyStatusInfoKeysArg *)gsimalloc(sizeof(GPGetBuddyStatusInfoKeysArg));
				callback.callback = anIterator->callback;
				callback.param = anIterator->userData;
				arg->keys = NULL;
				arg->numKeys = 0;
				arg->values = NULL;
				arg->profile = peer->profile;
				gpiAddCallback(connection, callback, arg, NULL, 0);
				
			}
			
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Misc, GSIDebugLevel_Notice, "Peer operation timed out");
			gpiPeerRemoveOp(peer, anIterator);
		}
		anIterator = anIterator->next;
	}
}