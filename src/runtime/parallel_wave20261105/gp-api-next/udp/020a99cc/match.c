#include "context.h"
GSUdpErrorCode native_main_020a99cc(unsigned short thePort, int theIncomingBufSize, 
									 int theOutgoingBufSize, gsUdpErrorCallback theAppNetworkError, 
									 gsUdpConnConnectedCallback theAppConnected,
									 gsUdpConnClosedCallback theAppClosed,
									 gsUdpConnPingCallback theAppPing,
									 gsUdpConnReceivedDataCallback theAppReceive,
									 gsUdpUnknownMsgCallback theAppUnownMsg,
									 gsUdpAppConnectAttemptCallback theAppConnectAttempt,
									 void *theAppUserData)
{
	int incomingBufferSize,
		outgoingBufferSize;
	char anAddr[GS_IP_ADDR_AND_PORT];
	GT2Result aGt2Result;
	
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	
	
	
	incomingBufferSize = theIncomingBufSize != 0 ? theIncomingBufSize : GS_UDP_DEFAULT_IN_BUFFSIZE;
	outgoingBufferSize = theOutgoingBufSize != 0 ? theOutgoingBufSize : GS_UDP_DEFAULT_OUT_BUFFSIZE;

	
	aUdp->mAppNetworkError = theAppNetworkError;
	aUdp->mAppUnknownMessage = theAppUnownMsg;
	aUdp->mAppConnected = theAppConnected;
	aUdp->mAppClosed = theAppClosed;
	aUdp->mAppPingReply = theAppPing;
	aUdp->mAppRecvData = theAppReceive;
	aUdp->mAppConnAttempt = theAppConnectAttempt;

	
	gt2AddressToString(0, thePort, anAddr);
	aGt2Result = gt2CreateSocket(&aUdp->mSocket, anAddr,  outgoingBufferSize, incomingBufferSize, 
		gsUdpSocketError);
	if (aGt2Result != GT2Success)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_WarmError, 
			"[Udp Engine] error creating gt2 socket, error code: %d\n", aGt2Result);
		return GS_UDP_NETWORK_ERROR;
	}	
	
	aUdp->mRemotePeers = ArrayNew(sizeof(GSUdpRemotePeer), 1, NULL);
	if (aUdp->mRemotePeers == NULL)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Memory, GSIDebugLevel_HotError, 
			"[Udp Engine] No more memory!!!\n");
		return GS_UDP_NO_MEMORY;
	}

	aUdp->mMsgHandlers = ArrayNew(sizeof(GSUdpMsgHandler), 1, gsUdpMsgHandlerFree);
	if (aUdp->mMsgHandlers == NULL)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Memory, GSIDebugLevel_HotError, 
			"[Udp Engine] No more memory!!!\n");
		return GS_UDP_NO_MEMORY;
	}
		
	
	
	gt2SetUnrecognizedMessageCallback(aUdp->mSocket, gsUdpUnrecognizedMsgCB);
	
	
	gt2Listen(aUdp->mSocket, gsUdpConnAttemptCB);
	aUdp->mLocalAddr = gt2GetLocalIP(aUdp->mSocket);
	aUdp->mLocalPort = gt2GetLocalPort(aUdp->mSocket);
	aUdp->mAppPendingConnections = 0;
	aUdp->mInitialized = gsi_true;
	if (theAppUserData)
	{
		aUdp->mAppUserData = theAppUserData;
	}
	else
		aUdp->mAppUserData = NULL;
	return GS_UDP_NO_ERROR;
}
