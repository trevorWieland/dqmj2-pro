#include "context.h"
GT2Bool native_main_020b3f00
(
	GT2Socket socket,
	GT2Connection connection,
	unsigned int ip,
	unsigned short port,
	GT2Bool reset,
	const GT2Byte * message,
	int len,
	GT2Bool send
)
{
	gt2DumpCallback callback;

	assert(socket);
	if(!socket)
		return GT2True;

	if(send)
		callback = socket->sendDumpCallback;
	else
		callback = socket->receiveDumpCallback;

	if(!callback)
		return GT2True;

	
	if(!len || !message)
	{
		message = NULL;
		len = 0;
	}

	socket->callbackLevel++;
	if(connection)
		connection->callbackLevel++;

	callback(socket, connection, ip, port, reset, message, len);

	socket->callbackLevel--;
	if(connection)
		connection->callbackLevel--;

	
	if(socket->close && !socket->callbackLevel)
	{
		gti2CloseSocket(socket);
		return GT2False;
	}

	return GT2True;
}
