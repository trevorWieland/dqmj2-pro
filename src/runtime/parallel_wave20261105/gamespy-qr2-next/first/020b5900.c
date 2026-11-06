#include "context.h"
GT2Bool native_main_020b5900(GT2Connection connection, GTI2OutgoingBufferMessage * message)
{
	GTI2MessageType type;
	int pos;
	pos = (message->start + connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN + 1 + 2);
	native_fn_020b45c8(connection->outgoingBuffer.buffer, pos, connection->expectedSerialNumber);
	if(!native_fn_020b4108(connection, connection->outgoingBuffer.buffer + message->start, message->len))
		return GT2False;
	message->lastSend = connection->lastSend;
	type = (GTI2MessageType)connection->outgoingBuffer.buffer[message->start + connection->socket->protocolOffset + GTI2_MAGIC_STRING_LEN];
	if(type == GTI2MsgServerChallenge)
		connection->challengeTime = connection->lastSend;
	return GT2True;
}
