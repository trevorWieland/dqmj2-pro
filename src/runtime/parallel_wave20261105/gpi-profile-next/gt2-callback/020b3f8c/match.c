#include "context.h"
GT2Bool native_main_020b3f8c
(
	GT2Socket socket,
	unsigned int ip,
	unsigned short port,
	GT2Byte * message,
	int len,
	GT2Bool * handled
)
{
	*handled = GT2False;

	assert(socket);
	if(!socket)
		return GT2True;

	if(!socket->unrecognizedMessageCallback)
		return GT2True;

	
	if(!len || !message)
	{
		message = NULL;
		len = 0;
	}

	socket->callbackLevel++;

	*handled = socket->unrecognizedMessageCallback(socket, ip, port, message, len);

	socket->callbackLevel--;

	
	if(socket->close && !socket->callbackLevel)
	{
		gti2CloseSocket(socket);
		return GT2False;
	}

	return GT2True;
}
