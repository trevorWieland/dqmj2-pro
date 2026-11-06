#include "context.h"
GT2Bool native_main_020b3ca4
(
	GT2Connection connection,
	GT2Result result,
	GT2Byte * message,
	int len
)
{
	assert(connection);
	if(!connection)
		return GT2True;
	
	
	connection->connectionResult = result;

	if(!connection->callbacks.connected)
		return GT2True;

	
	if(!len || !message)
	{
		message = NULL;
		len = 0;
	}

	connection->callbackLevel++;
	connection->socket->callbackLevel++;

	connection->callbacks.connected(connection, result, message, len);

	connection->callbackLevel--;
	connection->socket->callbackLevel--;

	
	if(connection->socket->close && !connection->socket->callbackLevel)
	{
		gti2CloseSocket(connection->socket);
		return GT2False;
	}

	return GT2True;
}
