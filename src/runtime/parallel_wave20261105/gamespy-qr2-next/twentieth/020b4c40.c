#include "context.h"
GT2Bool native_main_020b4c40(GT2Connection connection)
{
	GTI2IncomingBufferMessage * message;
	int num;
	int i;
restart:
	num = native_fn_020a8640(connection->incomingBufferMessages);
	for(i = (num - 1) ; i >= 0 ; i--)
	{
		message = (GTI2IncomingBufferMessage *)native_fn_020a8644(connection->incomingBufferMessages, i);
		if(message->serialNumber == connection->expectedSerialNumber)
		{
			if(!native_fn_020b4a30(connection, message->type, connection->incomingBuffer.buffer + message->start, message->len))
				return GT2False;
			native_fn_020b4be4(connection, message, i);
			goto restart;
		}
	}
	return GT2True;
}
