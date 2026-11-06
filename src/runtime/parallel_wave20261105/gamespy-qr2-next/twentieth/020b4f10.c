#include "context.h"
GT2Bool native_main_020b4f10(GT2Connection connection, GTI2MessageType type, GT2Byte * message, int len)
{
	int headerLength;
	GT2Byte * dataStart;
	int dataLen;
	headerLength = (connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN + 1);
	dataStart = (message + headerLength);
	dataLen = (len - headerLength);
	if(type == GTI2MsgAck)
	{
		if(!native_fn_020b4dbc(connection, dataStart, dataLen))
			return GT2False;
	}
	else if(type == GTI2MsgNack)
	{
		if(!native_fn_020b4df0(connection, dataStart, dataLen))
			return GT2False;
	}
	else if(type == GTI2MsgPing)
	{
		if(!native_fn_020b4e84(connection, message, len))
			return GT2False;
	}
	else if(type == GTI2MsgPong)
	{
		if(!native_fn_020b4e8c(connection, dataStart, dataLen))
			return GT2False;
	}
	else if(type == GTI2MsgClosed)
	{
		if(!native_fn_020b4ee8(connection))
			return GT2False;
	}
	return GT2True;
}
