#include "context.h"
GSUdpErrorCode native_main_020a9b08(unsigned int theIp, unsigned short thePort,
									  char theInitMsg[GS_UDP_MSG_HEADER_LEN], int timeOut)
{
	char anAddr[GS_IP_ADDR_AND_PORT];
	GSUdpRemotePeer aRemotePeer;	
	GSUdpMsgHandler aHandler;
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	GT2ConnectionCallbacks aCallbacks;
	int index;
	GS_ASSERT(aUdp->mInitialized);
	GS_ASSERT(theIp);
	GS_ASSERT(thePort);

	if (!aUdp->mInitialized)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Engine not initialized\n");
		return GS_UDP_NETWORK_ERROR;
	}
	
	if (theIp == 0 || thePort == 0)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Invalid parameter(s), check ip, port");
		return GS_UDP_PARAMETER_ERROR;
	}
	
	aRemotePeer.mAddr = theIp;  
	aRemotePeer.mPort = thePort;  

	index = ArraySearch(aUdp->mRemotePeers, &aRemotePeer, gsUdpRemotePeerCompare, 0, 0);
	if (index != NOT_FOUND)
	{
		GSUdpRemotePeer *aPeerFound = (GSUdpRemotePeer *)ArrayNth(aUdp->mRemotePeers, index);
		GT2ConnectionState aState = gt2GetConnectionState(aPeerFound->mConnection);
		if (aState == GT2Connected)
		{
			gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
				"[Udp Engine] Engine is already talking to remote address\n");
			return GS_UDP_ADDRESS_ALREADY_IN_USE;
		}
		else if (aState == GT2Connecting)
		{
			copy16(aHandler.mInitialMsg, theInitMsg, GS_UDP_MSG_HEADER_LEN);
			
			index = ArraySearch(aUdp->mMsgHandlers, &aHandler, gsUdpMsgHandlerCompare, 0, 0);
			if (index != NOT_FOUND)
			{
				GSUdpMsgHandler *aHandlerFound = (GSUdpMsgHandler *)ArrayNth(aUdp->mMsgHandlers, index);
				ArrayAppend(aHandlerFound->mPendingConnections, aPeerFound);
			}
		}
	}	
	else
	{
		gt2AddressToString(theIp, thePort, anAddr);
		aCallbacks.closed = gsUdpClosedRoutingCB;
		aCallbacks.connected = gsUdpConnectedRoutingCB;
		aCallbacks.ping = gsUdpPingRoutingCB;
		aCallbacks.received = gsUdpReceivedRoutingCB;

		
		gt2Connect(aUdp->mSocket, &aRemotePeer.mConnection, anAddr, (unsigned char *)theInitMsg, GS_UDP_MSG_HEADER_LEN, timeOut, &aCallbacks, GT2False);

		ArrayAppend(aUdp->mRemotePeers, &aRemotePeer);
		
		copy16(aHandler.mInitialMsg, theInitMsg, GS_UDP_MSG_HEADER_LEN);
		
		index = ArraySearch(aUdp->mMsgHandlers, &aHandler, gsUdpMsgHandlerCompare, 0, 0);
		if (index != NOT_FOUND)
		{
			GSUdpRemotePeer *aRemotePeerPtr = (GSUdpRemotePeer *)ArrayNth(aUdp->mRemotePeers, ArrayLength(aUdp->mRemotePeers) - 1);
			GSUdpMsgHandler *aHandlerFound = (GSUdpMsgHandler *)ArrayNth(aUdp->mMsgHandlers, index);
			ArrayAppend(aHandlerFound->mPendingConnections, &aRemotePeerPtr);
		}
		else
		{
			aUdp->mAppPendingConnections++;
		}
	}
	return GS_UDP_NO_ERROR;
}
