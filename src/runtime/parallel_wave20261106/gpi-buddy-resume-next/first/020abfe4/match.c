#include "context.h"
GPResult
native_main_020abfe4(
  GPConnection * connection,
  int profileid,
  int type,
  const char * message,
  int sendOption,
  GPIPeerOp *peerOp
)
{
	GPIPeer * peer;
	GPIProfile * profile;
	
	peer = gpiGetPeerByProfile(connection, profileid);
	if(!peer)
	{
		
		
		if(!gpiGetProfile(connection, profileid, &profile) ||
		   (!profile->buddyStatusInfo || !profile->buddyStatusInfo->buddyPort))
		{
			if (sendOption == GP_DONT_ROUTE)
				return GP_NETWORK_ERROR;
			return gpiSendServerBuddyMessage(connection, profileid, type, message);
		}

		
		
		peer = gpiAddPeer(connection, profileid, GPITrue);
		if(!peer)
			return GP_MEMORY_ERROR;

		
		
		if(!profile->peerSig)
		{
			
			
			CHECK_RESULT(gpiPeerGetSig(connection, peer));
		}
		else
		{
			
			
			CHECK_RESULT(gpiPeerStartConnect(connection, peer));
		}
	}
	else if (peer->state == GPI_PEER_DISCONNECTED)
	{
		if (gpiGetProfile(connection, profileid, &profile))
		{
			
			
			if (profile->buddyStatusInfo)
				profile->buddyStatusInfo->buddyPort = 0;

			
			if (sendOption == GP_DONT_ROUTE)
				return GP_NETWORK_ERROR;
			if (type < 100)
				return gpiSendServerBuddyMessage(connection, profileid, type, message);
		}
	}
	
	if (peerOp)
	{
		gpiPeerAddOp(peer, peerOp);
	}
	
	
	CHECK_RESULT(gpiPeerAddMessage(connection, peer, type, message));

	return GP_NO_ERROR;
}
