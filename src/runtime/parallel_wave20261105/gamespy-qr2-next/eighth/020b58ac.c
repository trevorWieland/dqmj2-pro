#include "context.h"
GT2Bool native_main_020b58ac(GT2Socket socket, unsigned int ip, unsigned short port)
{
	char buffer[MAX_PROTOCOL_OFFSET + GTI2_MAGIC_STRING_LEN + 1];
	int pos = 0;
	if (socket->protocolType == GTI2VdpProtocol)
	{
		short dataLength = GTI2_MAGIC_STRING_LEN + 1;
		memcpy(buffer, &dataLength, 2);
		pos += 2;
	}
	memcpy(buffer + pos, GTI2_MAGIC_STRING, GTI2_MAGIC_STRING_LEN);
	pos += GTI2_MAGIC_STRING_LEN;
	buffer[pos++] = GTI2MsgClosed;
	if(!native_fn_020b5d3c(socket, ip, port, (const GT2Byte *)buffer, pos))
		return GT2False;
	return GT2True;
}
