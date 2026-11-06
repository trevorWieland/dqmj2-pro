#include "context.h"
GT2Bool native_main_020b5344(GT2Connection connection, unsigned short SN, int len)
{
	GTI2OutgoingBufferMessage messageInfo = {0};
	int num;
	messageInfo.start = connection->outgoingBuffer.len;
	messageInfo.len = len;
	messageInfo.serialNumber = SN;
	messageInfo.lastSend = native_fn_020a8ef8();
	num = native_fn_020a8640(connection->outgoingBufferMessages);
	native_fn_020a865c(connection->outgoingBufferMessages, &messageInfo);
	if(native_fn_020a8640(connection->outgoingBufferMessages) != (num + 1))
		return GT2False;
	return GT2True;
}
