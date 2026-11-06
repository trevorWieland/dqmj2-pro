#include "context.h"
GT2Bool native_main_020b3d04
(
	GT2Connection connection,
	GT2Byte * message,
	int len,
	GT2Bool reliable
)
{
	assert(connection);
	if(!connection)
		return GT2True;

	if(!connection->callbacks.received)
		return GT2True;

	
	if(!len || !message)
	{
		message = NULL;
		len = 0;
	}

	connection->callbackLevel++;
	connection->socket->callbackLevel++;

	connection->callbacks.received(connection, message, len, reliable);

	connection->callbackLevel--;
	connection->socket->callbackLevel--;

	
	if(connection->socket->close && !connection->socket->callbackLevel)
	{
		gti2CloseSocket(connection->socket);
		return GT2False;
	}

	return GT2True;
}
