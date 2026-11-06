#include "context.h"
GPResult
native_main_020aab70(
  GPConnection * connection
)
{
	char * next;
	char * str;
	int id;
	GPIOperation * operation;
	char * tempPtr;
	int len;
	GPIBool connClosed = GPIFalse;
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPResult result;
	GPIBool loop;
	gsi_time now = current_time();
	do
	{
		gpiAddLocalInfo(connection, &iconnection->outputBuffer);
		if ( iconnection->outputBuffer.len > 0 )
			iconnection->kaTransmit = now;	
		CHECK_RESULT(gpiSendFromBuffer(connection, iconnection->cmSocket, &iconnection->outputBuffer, &connClosed, GPITrue, (char*)native_data_020e0548));
		result = gpiRecvToBuffer(connection, iconnection->cmSocket, &iconnection->socketBuffer, &len, &connClosed, (char*)native_data_020e0548);
		if(result != GP_NO_ERROR)
		{
			if(result == GP_NETWORK_ERROR)
				CallbackFatalError(connection, GP_NETWORK_ERROR, GP_NETWORK, native_data_020e054c);
			return result;
		}
		while((next = strstr(iconnection->socketBuffer.buffer, native_data_020e0578)) != NULL)
		{
			iconnection->kaTransmit = now;
			next[0] = '\0';
			gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_RawDump,
				"CMD: %s\n", iconnection->socketBuffer.buffer);
			len = (next - iconnection->socketBuffer.buffer);
			if(len > iconnection->inputBufferSize)
			{
				iconnection->inputBufferSize += max(GPI_READ_SIZE, len);
				tempPtr = (char*)gsirealloc(iconnection->inputBuffer, (unsigned int)iconnection->inputBufferSize + 1);
				if(tempPtr == NULL)
					Error(connection, GP_MEMORY_ERROR, native_data_020e0580);
				iconnection->inputBuffer = tempPtr;
			}
			memcpy(iconnection->inputBuffer, iconnection->socketBuffer.buffer, (unsigned int)len + 1);
			next += 7;
			iconnection->socketBuffer.len -= (next - iconnection->socketBuffer.buffer);
			memmove(iconnection->socketBuffer.buffer, next, (unsigned int)iconnection->socketBuffer.len + 1);
			str = strstr(iconnection->inputBuffer, native_data_020e0590);
			if(str != NULL)
			{
				id = atoi(str + 4);
				if(!gpiFindOperationByID(connection, &operation, id))
				{
					gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_HotError,
						"No matching operation found for id %d\n", id);
				}
				else
				{
					CHECK_RESULT(gpiProcessOperation(connection, operation, iconnection->inputBuffer));
				}
			}
			else
			{
				if(gpiCheckForError(connection, iconnection->inputBuffer, GPITrue))
				{
					return GP_SERVER_ERROR;
				}
				else if(strncmp(iconnection->inputBuffer, native_data_020e0598, 4) == 0)
				{
					CHECK_RESULT(gpiProcessRecvBuddyMessage(connection, iconnection->inputBuffer));
				}
				else if(strncmp(iconnection->inputBuffer, native_data_020e05a0, 4) == 0)
				{
				}
				else if(strncmp(iconnection->inputBuffer, native_data_020e05a8, 4) == 0)
				{
					gpiValueForKey(iconnection->inputBuffer, native_data_020e05a8, iconnection->loginTicket, sizeof(iconnection->loginTicket));
				}
				else if(strncmp(iconnection->inputBuffer, native_data_020e05b0, 5) == 0)
				{
					CHECK_RESULT(gpiProcessRecvBuddyStatusInfo(connection, iconnection->inputBuffer));
				}                
				else
				{
					gsDebugFormat(GSIDebugCat_GP, GSIDebugType_Network, GSIDebugLevel_HotError,
						"Received an unrecognized message.\n");
				}
			}
		}
		if(connClosed && iconnection->connectState != GPI_PROFILE_DELETING)
		{
			gpiSetError(connection, GP_CONNECTION_CLOSED, native_data_020e05b8);
			gpiCallErrorCallback(connection, GP_NETWORK_ERROR, GP_FATAL);
			return GP_NO_ERROR;
		}
		loop = gpiOperationsAreBlocking(connection);
		if(loop)
			msleep(10);
	}
	while(loop);
	if ( now - iconnection->kaTransmit > KEEPALIVE_TIMEOUT )
	{
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e05e0);
		iconnection->kaTransmit = now;
	}
	return GP_NO_ERROR;
}
