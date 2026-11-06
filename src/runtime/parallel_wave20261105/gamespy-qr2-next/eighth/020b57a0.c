#include "context.h"
GT2Bool native_main_020b57a0(GT2Connection connection)
{
	char buffer[MAX_PROTOCOL_OFFSET + GTI2_MAGIC_STRING_LEN + 1 + 2];
	int pos = 0;
	if (connection->socket->protocolType == GTI2VdpProtocol)
	{
		short dataLength = (GTI2_MAGIC_STRING_LEN + 1 + 2);
		memcpy(buffer, &dataLength, 2);
		pos += 2;
	}
	memcpy(buffer + pos, GTI2_MAGIC_STRING, GTI2_MAGIC_STRING_LEN);
	pos += GTI2_MAGIC_STRING_LEN;
	buffer[pos++] = GTI2MsgAck;
	native_fn_020b45c8((GT2Byte *)buffer, pos, connection->expectedSerialNumber);
	pos += 2;
	if(!native_fn_020b4108(connection, (const GT2Byte *)buffer, pos))
		return GT2False;
	connection->pendingAck = GT2False;
	return GT2True;
}
