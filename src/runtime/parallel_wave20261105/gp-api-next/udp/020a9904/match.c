#include "context.h"
void native_main_020a9904(GT2Socket socket, GT2Connection connection, unsigned int ip, 
						unsigned short port, int latency, GT2Byte * message, int len)
{
	
	int index;
	GSUdpMsgHandler aHandler;
	GSUdpRemotePeer aRemotePeer;
	GSUdpEngineObject *aUdp = gsUdpEngineGetEngine();
	char anAddr[GS_IP_ADDR_AND_PORT];
	
	gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Comment, 
		"[Udp Engine] Connection attempt from %s\n", gt2AddressToString(ip, port, anAddr));
	
	
	if (len >= GS_UDP_MSG_HEADER_LEN)
	{    
		copy16(aHandler.mInitialMsg, message, GS_UDP_MSG_HEADER_LEN);
		
		aRemotePeer.mAddr = ip;
		aRemotePeer.mPort = port;
		aRemotePeer.mConnection = connection;
		
		ArrayAppend(aUdp->mRemotePeers, &aRemotePeer);
		index = ArraySearch(aUdp->mMsgHandlers, &aHandler, gsUdpMsgHandlerCompare, 0, 0);
		if (index != NOT_FOUND)
		{
			GT2ConnectionCallbacks aCallbacks;
			
			aCallbacks.closed = gsUdpClosedRoutingCB;
			aCallbacks.connected = gsUdpConnectedRoutingCB;
			aCallbacks.ping = gsUdpPingRoutingCB;
			aCallbacks.received = gsUdpReceivedRoutingCB;

	       
			
			gt2Accept(aRemotePeer.mConnection, &aCallbacks);	
			gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Comment, 
				"[Udp Engine] Connection attempt auto-accepted for message handler\n");
			return;
		}
	}
	
	if (aUdp->mAppConnAttempt) 
	{
		gsDebugFormat(GSIDebugCat_Common, GSIDebugType_Network, GSIDebugLevel_Comment, 
			"[Udp Engine] Connection attempt from %s, asking app to accept/reject\n", gt2AddressToString(ip, port, anAddr));
		aUdp->mAppConnAttempt(ip, port, latency, (unsigned char *)message, (unsigned int)len, aUdp->mAppUserData);
	}
	else 
	{
		
		gt2Reject(connection, NULL, 0);
		ArrayRemoveAt(aUdp->mRemotePeers, ArrayLength(aUdp->mRemotePeers) -1);
	}
	GSI_UNUSED(socket);
	GSI_UNUSED(anAddr);
}
