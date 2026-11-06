#include "context.h"
GSUdpErrorCode native_main_020a9aa8(unsigned int theIp, unsigned short thePort, GSUdpPeerState *thePeerState)
{
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	GSUdpRemotePeer aPeer, *aPeerFound;
	int index;
	GS_ASSERT(aUdp->mInitialized);
	GS_ASSERT(theIp);
	GS_ASSERT(thePort);
	GS_ASSERT(thePeerState != NULL);
	if (!aUdp->mInitialized)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_State, GSIDebugLevel_Debug, 
			"[Udp Engine] Engine not initialized\n");
		*thePeerState = GS_UDP_PEER_CLOSED;
		return GS_UDP_NOT_INITIALIZED;
	}

	aPeer.mAddr = theIp;
	aPeer.mPort = thePort;
	index = ArraySearch(aUdp->mRemotePeers, &aPeer, gsUdpRemotePeerCompare, 0, 0);
	if (index == NOT_FOUND)
	{
		*thePeerState = GS_UDP_PEER_CLOSED;
		return GS_UDP_NO_ERROR;
	}
	
	aPeerFound = (GSUdpRemotePeer *)ArrayNth(aUdp->mRemotePeers, index);

	*thePeerState = (GSUdpPeerState)gt2GetConnectionState(aPeerFound->mConnection);
	return GS_UDP_NO_ERROR;
}
