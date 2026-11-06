#include "context.h"
GT2Bool native_main_020b4194(GT2Connection connection, gsi_time now)
{
	int i;
	int len;
	GTI2OutgoingBufferMessage * message;
	len = native_fn_020a8640(connection->outgoingBufferMessages);
	for(i = 0 ; i < len ; i++)
	{
		message = (GTI2OutgoingBufferMessage *)native_fn_020a8644(connection->outgoingBufferMessages, i);
		if((now - message->lastSend) > GTI2_RESEND_TIME)
		{
			if(!native_fn_020b5900(connection, message))
				return GT2False;
		}
	}
	return GT2True;
}
