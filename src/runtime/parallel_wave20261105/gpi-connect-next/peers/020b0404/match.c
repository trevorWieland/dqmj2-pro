#include "context.h"
GPIPeer*
native_main_020b0404(
  GPConnection * connection,
  int profileid,
  GPIBool initiate
)
{
	GPIPeer * peer;
	GPIConnection * iconnection = (GPIConnection*)*connection;

	
	
	peer = (GPIPeer *)gsimalloc(sizeof(GPIPeer));
	if(peer == NULL)
		return NULL;
	memset(peer, 0, sizeof(GPIPeer));
	peer->state = GPI_PEER_NOT_CONNECTED;
	peer->initiated = initiate;
	
	peer->profile = profileid;
	peer->timeout = (time(NULL) + GPI_PEER_TIMEOUT);
	peer->pnext = iconnection->peerList;
	peer->messages = ArrayNew(sizeof(GPIMessage), 0, gpiFreeMessage);
	iconnection->peerList = peer;
	peer->peerOpQueue.first = NULL;
	peer->peerOpQueue.last = NULL;
	peer->peerOpQueue.opList = NULL;
	return peer;
}