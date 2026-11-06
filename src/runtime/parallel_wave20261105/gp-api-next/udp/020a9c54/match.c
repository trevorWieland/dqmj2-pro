#include "context.h"
GSUdpErrorCode native_main_020a9c54(unsigned int theIp, unsigned short thePort, 
									  char theHeader[GS_UDP_MSG_HEADER_LEN], unsigned char *theMsg, 
									  unsigned int theMsgLen, gsi_bool theReliable)
{
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	int aTotalMessageLen, index;
	GSUdpRemotePeer aRemotePeer, *aRemotePeerFound;
	GT2Byte *fullMessage;
	GT2Result aResult;
	GS_ASSERT(aUdp->mInitialized);
	GS_ASSERT(theIp);
	GS_ASSERT(thePort);
	if (!aUdp->mInitialized)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Debug,
			"[Udp Engine] Engine not initialized\n");
		return GS_UDP_NETWORK_ERROR;
	}

	
	if (!theHeader[0])
		aTotalMessageLen = (int)theMsgLen;
	else 
		aTotalMessageLen = (int)(GS_UDP_MSG_HEADER_LEN + theMsgLen);

	aRemotePeer.mAddr = theIp;
	aRemotePeer.mPort = thePort;

	index = ArraySearch(aUdp->mRemotePeers, &aRemotePeer, gsUdpRemotePeerCompare, 0, 0);
	if (index == NOT_FOUND)
	{
		char anAddr[GS_IP_ADDR_AND_PORT];
		gt2AddressToString(theIp, thePort, anAddr);
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"[Udp Engine] address not found for sending message\n", anAddr);
		return GS_UDP_ADDRESS_ERROR;
	}
	else
	{
		aRemotePeerFound = (GSUdpRemotePeer *)ArrayNth(aUdp->mRemotePeers, index);
	}

	if (aTotalMessageLen > gt2GetOutgoingBufferSize(aRemotePeerFound->mConnection) && theReliable)
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"[Udp Engine] Message Size too large, dropping message\n");
		return GS_UDP_MSG_TOO_BIG;
	}

	fullMessage = (GT2Byte *)gsimalloc((unsigned long)aTotalMessageLen);
	copy16(fullMessage, theHeader, GS_UDP_MSG_HEADER_LEN);
	memcpy(fullMessage + GS_UDP_MSG_HEADER_LEN, theMsg, theMsgLen);
	
	
	aResult = gt2Send(aRemotePeerFound->mConnection, fullMessage, aTotalMessageLen, theReliable);
	gsifree(fullMessage);

	if (aResult != GT2Success)
		return GS_UDP_SEND_FAILED;
	return GS_UDP_NO_ERROR;
}
