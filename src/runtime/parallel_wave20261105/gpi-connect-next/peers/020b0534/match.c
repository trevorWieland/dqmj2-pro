#include "context.h"
GPResult
native_main_020b0534(
  GPConnection * connection,
  GPIPeer * peer,
  int type,
  const char * message
)
{
	GPIMessage gpiMessage;
	int len;

	GS_ASSERT(peer != NULL);
	GS_ASSERT(message != NULL);
	
	if (peer == NULL)
		return GP_NETWORK_ERROR;
	if (message == NULL)
		return GP_NETWORK_ERROR;

	
	
	len = (int)strlen(message);

	
	
	memset(&gpiMessage, 0, sizeof(GPIMessage));

	
	
	gpiMessage.type = type;

	
	
	CHECK_RESULT(gpiAppendStringToBuffer(connection, &gpiMessage.buffer, native_data_020e1098));
	CHECK_RESULT(gpiAppendIntToBuffer(connection, &gpiMessage.buffer, type));
	CHECK_RESULT(gpiAppendStringToBuffer(connection, &gpiMessage.buffer, native_data_020e109c));
	CHECK_RESULT(gpiAppendIntToBuffer(connection, &gpiMessage.buffer, len));
	CHECK_RESULT(gpiAppendStringToBuffer(connection, &gpiMessage.buffer, native_data_020e10a4));

	
	
	gpiMessage.start = gpiMessage.buffer.len;
	CHECK_RESULT(gpiAppendStringToBufferLen(connection, &gpiMessage.buffer, message, len));
	CHECK_RESULT(gpiAppendCharToBuffer(connection, &gpiMessage.buffer, '\0'));

	
	
	ArrayAppend(peer->messages, &gpiMessage);

	
	
	peer->timeout = (time(NULL) + GPI_PEER_TIMEOUT);

	return GP_NO_ERROR;
}