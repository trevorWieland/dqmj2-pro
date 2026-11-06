#include "context.h"
GPResult
native_main_020acf00(
  GPConnection * connection,
  GPIOperation * operation
)
{
	struct sockaddr_in address;
	int rcode;
	
	GPIConnection * iconnection = (GPIConnection*)*connection;
	struct hostent * host;
	
	GSUdpErrorCode anError;
	strncpy(iconnection->mHeader, GPI_UDP_HEADER, GS_UDP_MSG_HEADER_LEN);

	if (!gsUdpEngineIsInitialized())
	{
		unsigned short peerPort = GPI_PEER_PORT;
		gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_Notice, 
			"Initializing UDP Layer\n");
		anError = gsUdpEngineInitialize(peerPort, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
		if (anError != GS_UDP_NO_ERROR)
		{
			while (anError != GS_UDP_NO_ERROR && peerPort < GPI_PEER_PORT + 100)
			{
				gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_Comment, 
					"Port %d failed, trying next port\n", peerPort);
				anError = gsUdpEngineInitialize(++peerPort, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
			}
			if (anError != GS_UDP_NO_ERROR)
			{
				gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_HotError, 
					"Tryed all 100 ports after default port, giving up.\n");
				CallbackFatalError(connection, GP_NETWORK_ERROR, GP_UDP_LAYER, 
					native_data_020e08dc);
			}
		}	
		if (!iconnection->firewall)
		{
			iconnection->peerPort = peerPort;
		}
	}
	else
	{
		gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_Notice, 
			"UDP Layer already initialized, using existing port.\n");
		iconnection->peerPort = gsUdpEngineGetLocalPort();
	}
	anError = gsUdpEngineAddMsgHandler(iconnection->mHeader, iconnection->mHeader, NULL, gpiPeerAcceptedCallback, gpiPeerLeftCallback, 
		gpiPeerPingReplyCallback, gpiPeerMessageCallback, connection);
	if (anError != GS_UDP_NO_ERROR)
	{
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_UDP_LAYER, native_data_020e0904);
	}
	if(iconnection->firewall)
	{
		
		
		
			
		iconnection->peerPort = 0;
	}
	
	

	
	
	
	iconnection->cmSocket = socket(AF_INET, SOCK_STREAM, 0);
	if(iconnection->cmSocket == INVALID_SOCKET)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e0930);

	
	
	rcode = SetSockBlocking(iconnection->cmSocket,0);
	if(rcode == 0)
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e0958);

	memset(&address, 0, sizeof(address));
	address.sin_family = AF_INET;
	
	
	if (inet_addr(GPConnectionManagerHostname) == INADDR_NONE)
	{
		host = gethostbyname(GPConnectionManagerHostname);
		if(host == NULL)
			CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e098c);
		address.sin_addr.s_addr = *(unsigned int *)host->h_addr_list[0];
		
	}
	else
	{
		address.sin_addr.s_addr = inet_addr(GPConnectionManagerHostname);
		
	}

	
	
	assert(address.sin_addr.s_addr != 0);
	address.sin_port = htons(GPI_CONNECTION_MANAGER_PORT);
	rcode = connect(iconnection->cmSocket, (struct sockaddr *)&address, sizeof(struct sockaddr_in));
	if (gsiSocketIsError(rcode))
	{
		int error = GOAGetLastError(iconnection->cmSocket);
		if((error != WSAEWOULDBLOCK) && (error != WSAEINPROGRESS) && (error != WSAETIMEDOUT))
		{
			CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e09c0);
		}
	}

	
	
	operation->state = GPI_CONNECTING;
	iconnection->connectState = GPI_CONNECTING;

	return GP_NO_ERROR;
}
