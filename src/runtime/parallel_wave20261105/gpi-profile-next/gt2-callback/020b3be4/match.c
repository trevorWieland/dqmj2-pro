#include "context.h"
GT2Bool native_main_020b3be4
(
	GT2Socket socket
)
{
	assert(socket);
	if(!socket)
		return GT2True;

	if(!socket->socketErrorCallback)
		return GT2True;

	socket->callbackLevel++;

	socket->socketErrorCallback(socket);

	socket->callbackLevel--;

	
	if(socket->close && !socket->callbackLevel)
	{
		gti2CloseSocket(socket);
		return GT2False;
	}

	return GT2True;
}
