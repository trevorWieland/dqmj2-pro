#include "context.h"
GT2Bool native_main_020b3c24
(
	GT2Socket socket,
	GT2Connection connection,
	unsigned int ip,
	unsigned short port,
	int latency,
	GT2Byte * message,
	int len
)
{
	assert(socket && connection);
	if(!socket || !connection)
		return GT2True;

	if(!socket->connectAttemptCallback)
		return GT2True;

	
	if(!len || !message)
	{
		message = NULL;
		len = 0;
	}

	socket->callbackLevel++;
	connection->callbackLevel++;

	socket->connectAttemptCallback(socket, connection, ip, port, latency, message, len);

	socket->callbackLevel--;
	connection->callbackLevel--;

	
	if(socket->close && !socket->callbackLevel)
	{
		gti2CloseSocket(socket);
		return GT2False;
	}

	return GT2True;
}
