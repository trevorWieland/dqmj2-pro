#include "context.h"
GT2Bool native_main_020b4ad4(GT2Connection connection, GTI2MessageType type, unsigned short SN, GT2Byte * message, int len, GT2Bool * overflow)
{
	GTI2IncomingBufferMessage messageInfo;
	GTI2IncomingBufferMessage * bufferedMessage;
	int num;
	int i;
	num = native_fn_020a8640(connection->incomingBufferMessages);
	for(i = 0 ; i < num ; i++)
	{
		bufferedMessage = (GTI2IncomingBufferMessage *)native_fn_020a8644(connection->incomingBufferMessages, i);
		if(bufferedMessage->serialNumber == SN)
		{
			*overflow = GT2False;
			return GT2True;
		}
		if(native_fn_020b45d4(bufferedMessage->serialNumber, SN) > 0)
			break;
	}
	if(native_fn_020b3b50(&connection->incomingBuffer) < len)
	{
		*overflow = GT2True;
		return GT2True;
	}
	messageInfo.start = connection->incomingBuffer.len;
	messageInfo.len = len;
	messageInfo.type = type;
	messageInfo.serialNumber = SN;
	native_fn_020a86b8(connection->incomingBufferMessages, &messageInfo, native_fn_020b4ac8);
	if(native_fn_020a8640(connection->incomingBufferMessages) != (num + 1))
	{
		*overflow = GT2True;
		return GT2True;
	}
	native_fn_020b3b80(&connection->incomingBuffer, message, len);
	if(num == 0)
	{
		if(!native_fn_020b5810(connection, connection->expectedSerialNumber, (unsigned short)(SN - 1)))
			return GT2False;
	}
	else
	{
		GTI2IncomingBufferMessage * msg;
		msg = (GTI2IncomingBufferMessage *)native_fn_020a8644(connection->incomingBufferMessages, num);
		if(msg->serialNumber == SN)
		{
			GTI2IncomingBufferMessage * prev;
			unsigned short diff;
			prev = (GTI2IncomingBufferMessage *)native_fn_020a8644(connection->incomingBufferMessages, num - 1);
			diff = (unsigned short)native_fn_020b45d4(SN, prev->serialNumber);
			if(diff > 1)
			{
				if(!native_fn_020b5810(connection, (unsigned short)(prev->serialNumber + 1), (unsigned short)(SN - 1)))
					return GT2False;
			}
		}
	}
	*overflow = GT2False;
	return GT2True;
}
