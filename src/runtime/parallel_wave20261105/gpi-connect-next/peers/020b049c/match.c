#include "context.h"
GPResult
native_main_020b049c(
  GPConnection * connection,
  GPIPeer * peer
)
{
	
	
	GPIProfile * profile;
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GSUdpErrorCode anError;

	
	
	if(!gpiGetProfile(connection, peer->profile, &profile))
		Error(connection, GP_NETWORK_ERROR, native_data_020e0fac);

	

	if (profile->buddyStatusInfo)
	{
		GSUdpPeerState aPeerState;
		gsUdpEngineGetPeerState(profile->buddyStatusInfo->buddyIp , profile->buddyStatusInfo->buddyPort, &aPeerState);
		if (aPeerState != GS_UDP_PEER_CONNECTED || aPeerState != GS_UDP_PEER_CONNECTING)
		{
			anError = gsUdpEngineStartTalkingToPeer(profile->buddyStatusInfo->buddyIp , profile->buddyStatusInfo->buddyPort, 
			iconnection->mHeader, GPI_PEER_TIMEOUT);
			if (anError != GS_UDP_ADDRESS_ALREADY_IN_USE)
				CallbackError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e1060);
		}
		peer->ip = profile->buddyStatusInfo->buddyIp;
		peer->port = profile->buddyStatusInfo->buddyPort;
	}
	
	
	peer->state = GPI_PEER_CONNECTING;

	return GP_NO_ERROR;
}