#include "context.h"
GT2Bool native_main_020b3d60
(
	GT2Connection connection,
	GT2CloseReason reason
)
{
	assert(connection);
	if(!connection)
		return GT2True;

	if(!connection->callbacks.closed)
		return GT2True;

	connection->callbackLevel++;
	connection->socket->callbackLevel++;

	connection->callbacks.closed(connection, reason);

	connection->callbackLevel--;
	connection->socket->callbackLevel--;

	
	if(connection->socket->close && !connection->socket->callbackLevel)
	{
		gti2CloseSocket(connection->socket);
		return GT2False;
	}

	return GT2True;
}
