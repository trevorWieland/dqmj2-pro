#include "context.h"
GT2Bool native_main_020b4df0(GT2Connection connection, const GT2Byte * message, int len)
{
	unsigned short SNMin;
	unsigned short SNMax;
	int num;
	int i;
	GTI2OutgoingBufferMessage * messageInfo;
	SNMin = native_fn_020b45b0(message, 0);
	if(len == 2)
	{
		SNMax = SNMin;
	}
	else if(len == 4)
	{
		SNMax = native_fn_020b45b0(message, 2);
	}
	else
	{
		if(!native_fn_020b4634(connection))
			return GT2False;
		return GT2True;
	}
	num = native_fn_020a8640(connection->outgoingBufferMessages);
	for(i = 0 ; i < num ; i++)
	{
		messageInfo = (GTI2OutgoingBufferMessage *)native_fn_020a8644(connection->outgoingBufferMessages, i);
		if((native_fn_020b45d4(messageInfo->serialNumber, SNMin) >= 0) && (native_fn_020b45d4(messageInfo->serialNumber, SNMax) <= 0))
		{
			if(!native_fn_020b5900(connection, messageInfo))
				return GT2False;
		}
	}
	return GT2True;
}
