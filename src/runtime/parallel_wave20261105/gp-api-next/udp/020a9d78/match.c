#include "context.h"
GSUdpErrorCode native_main_020a9d78(char theInitMsg[GS_UDP_MSG_HEADER_LEN], char theHeader[GS_UDP_MSG_HEADER_LEN], 
									    gsUdpErrorCallback theMsgHandlerError, 
									    gsUdpConnConnectedCallback theMsgHandlerConnected, 
									    gsUdpConnClosedCallback theMsgHandlerClosed, 
									    gsUdpConnPingCallback theMsgHandlerPing,
										gsUdpConnReceivedDataCallback theMsgHandlerRecv,
										void *theUserData)
{
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	GSUdpMsgHandler aMsgHandler;
	GS_ASSERT(aUdp->mInitialized);
	GS_ASSERT(theInitMsg || theInitMsg[0]);
	GS_ASSERT(theHeader || theHeader[0]);
	if (!aUdp->mInitialized)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Engine not initialized\n");
		return GS_UDP_NETWORK_ERROR;
	}
	
	
	
	
	if (!theInitMsg[0])
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Invalid init message\n");
		return GS_UDP_PARAMETER_ERROR;
	}

	if (!theHeader[0])
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Invalid header\n");
		return GS_UDP_PARAMETER_ERROR;
	}

	
	
	aMsgHandler.mClosed = theMsgHandlerClosed;
	aMsgHandler.mConnected = theMsgHandlerConnected;
	aMsgHandler.mPingReply = theMsgHandlerPing;
	aMsgHandler.mReceived = theMsgHandlerRecv;
	
	aMsgHandler.mNetworkError = theMsgHandlerError;

	copy16(aMsgHandler.mInitialMsg, theInitMsg, GS_UDP_MSG_HEADER_LEN);
	copy16(aMsgHandler.mHeader, theHeader, GS_UDP_MSG_HEADER_LEN);
		
	aMsgHandler.mPendingConnections = ArrayNew(sizeof(GSUdpRemotePeer *), 1, NULL);
	if (aMsgHandler.mPendingConnections == NULL)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Memory, GSIDebugLevel_HotError, 
			"[Udp Engine] No more memory!!!\n");
		return GS_UDP_NO_MEMORY;
	}
	aMsgHandler.mUserData = theUserData;
	ArrayAppend(aUdp->mMsgHandlers, &aMsgHandler);
	
	return GS_UDP_NO_ERROR;
}
