#include "context.h"
GT2Bool native_main_020b3db0
(
	GT2Connection connection,
	int latency
)
{
	assert(connection);
	if(!connection)
		return GT2True;

	if(!connection->callbacks.ping)
		return GT2True;

	connection->callbackLevel++;
	connection->socket->callbackLevel++;

	connection->callbacks.ping(connection, latency);

	connection->callbackLevel--;
	connection->socket->callbackLevel--;

	
	if(connection->socket->close && !connection->socket->callbackLevel)
	{
		gti2CloseSocket(connection->socket);
		return GT2False;
	}

	return GT2True;
}
