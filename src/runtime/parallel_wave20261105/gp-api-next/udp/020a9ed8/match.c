#include "context.h"
int native_main_020a9ed8(unsigned int theIp, unsigned short thePort)
{
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	GSUdpRemotePeer aRemotePeer, *aRemotePeerFound;
	int index;
	GS_ASSERT(aUdp->mInitialized);
	GS_ASSERT(theIp);
	GS_ASSERT(thePort);
	if (!aUdp->mInitialized)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Engine not initialized\n");
		return 0;
	}

	aRemotePeer.mAddr = theIp;
	aRemotePeer.mPort = thePort;
	index = ArraySearch(aUdp->mRemotePeers, &aRemotePeer, gsUdpRemotePeerCompare, 0, 0);
	if (index != NOT_FOUND)
	{
		aRemotePeerFound = (GSUdpRemotePeer *)ArrayNth(aUdp->mRemotePeers, index);
		return gt2GetOutgoingBufferFreeSpace(aRemotePeerFound->mConnection);
	}
	return 0;
}
