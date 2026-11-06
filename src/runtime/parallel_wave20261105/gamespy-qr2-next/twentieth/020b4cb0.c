#include "context.h"
GT2Bool native_main_020b4cb0(GT2Connection connection, GTI2MessageType type, GT2Byte * message, int len)
{
	unsigned short SN;
	unsigned short ESN;
	const int headerLength = connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN + 1 + 2 + 2;
	GT2Bool overflow;
	if(len < (connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN + 1 + 2 + 2))
	{
		if(!native_fn_020b4634(connection))
			return GT2False;
		return GT2True;
	}
	SN = native_fn_020b45b0(message + connection->socket->protocolOffset, GTI2_MAGIC_STRING_LEN + 1);
	ESN = native_fn_020b45b0(message + connection->socket->protocolOffset, GTI2_MAGIC_STRING_LEN + 3);
	if (connection->socket->protocolType == GTI2VdpProtocol && type == GTI2MsgAppReliable)
	{
		message[connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN + 3] = message[0];
		message[connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN + 4] = message[1];
		message += headerLength - connection->socket->protocolOffset;
		len -= headerLength - connection->socket->protocolOffset;
	}
	else
	{
		message += headerLength;
		len -= headerLength;
	}
	if(!native_fn_020b465c(connection, ESN))
		return GT2False;
	if(SN == connection->expectedSerialNumber)
	{
		native_fn_020b4c90(connection);
		if(!native_fn_020b4a30(connection, type, message, len))
			return GT2False;
		if(!native_fn_020b4c40(connection))
			return GT2False;
		return GT2True;
	}
	if(native_fn_020b45d4(SN, connection->expectedSerialNumber) < 0)
	{
		native_fn_020b4c90(connection);
		return GT2True;
	}
	if(!native_fn_020b4ad4(connection, type, SN, message, len, &overflow))
		return GT2False;
	if(overflow)
	{
		if(!native_fn_020b4640(connection))
			return GT2False;
	}
	return GT2True;
}
