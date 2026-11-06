#include "context.h"
GPResult
native_main_020aa9b4(
  GPConnection * connection
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPResult result;
	iconnection->nick[0] = '\0';
	iconnection->uniquenick[0] = '\0';
	iconnection->email[0] = '\0';
	iconnection->cmSocket = INVALID_SOCKET;
	iconnection->connectState = GPI_NOT_CONNECTED;

	iconnection->socketBuffer.len = 0;
	iconnection->socketBuffer.pos = 0;
	iconnection->socketBuffer.size = 0;
	freeclear(iconnection->socketBuffer.buffer);
	iconnection->socketBuffer.buffer = NULL;

	iconnection->inputBufferSize = 0;
	freeclear(iconnection->inputBuffer);
	iconnection->inputBuffer = NULL;

	iconnection->outputBuffer.len = 0;
	iconnection->outputBuffer.pos = 0;
	iconnection->outputBuffer.size = 0;
	freeclear(iconnection->outputBuffer.buffer);
	iconnection->outputBuffer.buffer = NULL;

	iconnection->updateproBuffer.len = 0;
	iconnection->updateproBuffer.pos = 0;
	iconnection->updateproBuffer.size = 0;
	freeclear(iconnection->updateproBuffer.buffer);
	iconnection->updateproBuffer.buffer = NULL;

	iconnection->updateuiBuffer.len = 0;
	iconnection->updateuiBuffer.pos = 0;
	iconnection->updateuiBuffer.size = 0;
	freeclear(iconnection->updateuiBuffer.buffer);
	iconnection->updateuiBuffer.buffer = NULL;
	gpiStatusInfoKeysDestroy(connection);
	result = gpiStatusInfoKeysInit((GPConnection *)&iconnection);
	if (result != GP_NO_ERROR)
	{
		gpiDestroy((GPConnection *)&iconnection);
		return result;
	}
	
	iconnection->nextOperationID = 2;
	while(iconnection->operationList != NULL)
		gpiRemoveOperation(connection, iconnection->operationList);
	iconnection->operationList = NULL;
	iconnection->profileList.numBuddies = 0;
    
	gpiProfileMap(connection, gpiResetProfile, NULL);
	iconnection->userid = 0;
	iconnection->profileid = 0;
	iconnection->sessKey = 0;
	iconnection->numSearches = 0;
	iconnection->fatalError = GPIFalse;
	iconnection->peerList = NULL;
	iconnection->lastStatusState = (GPEnum)-1;
	iconnection->lastStatusString[0] = '\0';
	iconnection->lastLocationString[0] = '\0';
	iconnection->kaTransmit = 0;



	return GP_NO_ERROR;
}
