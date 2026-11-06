#include "context.h"
GT2Bool native_main_020b5390(GT2Connection connection, GTI2MessageType type, int len, GT2Bool * overflow)
{
	int freeSpace;
	unsigned short vdpDataLength = (unsigned short)(len - connection->socket->protocolOffset);
	freeSpace = native_fn_020b3b50(&connection->outgoingBuffer);
	if(freeSpace < len)
	{
		if(!native_fn_020b4640(connection))
			return GT2False;
		*overflow = GT2True;
		return GT2True;
	}
	if(!native_fn_020b5344(connection, connection->serialNumber, len))
	{
		if(!native_fn_020b4640(connection))
			return GT2False;
		*overflow = GT2True;
		return GT2True;
	}
	if (connection->socket->protocolType == GTI2VdpProtocol)
		native_fn_020b3b80(&connection->outgoingBuffer, (const GT2Byte *)&vdpDataLength, connection->socket->protocolOffset);
	native_fn_020b3b80(&connection->outgoingBuffer, (const GT2Byte *)GTI2_MAGIC_STRING, GTI2_MAGIC_STRING_LEN);
	native_fn_020b3b58(&connection->outgoingBuffer, (GT2Byte)type);
	native_fn_020b3b64(&connection->outgoingBuffer, connection->serialNumber++);
	native_fn_020b3b64(&connection->outgoingBuffer, connection->expectedSerialNumber);
	*overflow = GT2False;
	return GT2True;
}
