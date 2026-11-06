#include "context.h"
GT2Bool native_main_020b3e80
(
	GT2Connection connection,
	int filterID,
	GT2Byte * message,
	int len,
	GT2Bool reliable
)
{
	gt2ReceiveFilterCallback * callback;

	assert(connection);
	if(!connection)
		return GT2True;

	callback = (gt2ReceiveFilterCallback *)ArrayNth(connection->receiveFilters, filterID);
	if(!callback)
		return GT2True;

	
	if(!len || !message)
	{
		message = NULL;
		len = 0;
	}

	connection->callbackLevel++;
	connection->socket->callbackLevel++;

	(*callback)(connection, filterID, message, len, reliable);

	connection->callbackLevel--;
	connection->socket->callbackLevel--;

	
	if(connection->socket->close && !connection->socket->callbackLevel)
	{
		gti2CloseSocket(connection->socket);
		return GT2False;
	}

	return GT2True;
}
