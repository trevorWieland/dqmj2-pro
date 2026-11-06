#include "context.h"
void
native_main_020ade3c(
  GPConnection * connection,
  GPIBool tellServer
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIPeer * peer;
	GPIPeer * delPeer;
	GPIBool connClosed;

	
	
	
	if(iconnection->connectState == GPI_DISCONNECTED)
		return;

	
	
	
	if(iconnection->connectState != GPI_NOT_CONNECTED)
	{
		
		
		if(tellServer && (iconnection->connectState == GPI_CONNECTED))
		{
			
			
			gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0c54);
			gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->sessKey);
			gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b30);
		}

		
		
		
		gpiSendFromBuffer(connection, iconnection->cmSocket, &iconnection->outputBuffer, &connClosed, GPITrue, native_data_020e0c68);

		
		
		if(iconnection->cmSocket != INVALID_SOCKET)
		{
			shutdown(iconnection->cmSocket, 2);
			closesocket(iconnection->cmSocket);
			iconnection->cmSocket = INVALID_SOCKET;
		}
		
		iconnection->connectState = GPI_DISCONNECTED;

		
		
		iconnection->userid = 0;
		iconnection->profileid = 0;
		}
	if( gsUdpEngineIsInitialized())
		{
			
			
			
			gsUdpEngineRemoveMsgHandler(iconnection->mHeader);
			if (gsUdpEngineNoMoreMsgHandlers() && gsUdpEngineNoApp())
				gsUdpEngineShutdown();
		}

		
		
		
	
	
	
	
	freeclear(iconnection->socketBuffer.buffer);
	freeclear(iconnection->inputBuffer);
	freeclear(iconnection->outputBuffer.buffer);
	freeclear(iconnection->updateproBuffer.buffer);
	freeclear(iconnection->updateuiBuffer.buffer);
	while(iconnection->operationList != NULL)
		gpiRemoveOperation(connection, iconnection->operationList);
	iconnection->operationList = NULL;
	for(peer = iconnection->peerList ; peer != NULL ; )
	{
		delPeer = peer;
		peer = peer->pnext;
		gpiDestroyPeer(connection, delPeer);
	}
	iconnection->peerList = NULL;
	
	
	
	
	
	while(!gpiProfileMap(connection, gpiDisconnectCleanupProfile, NULL))  { };
}