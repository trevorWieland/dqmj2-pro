#include "context.h"
GPResult
native_main_020ac954(
  GPConnection * connection,
  SOCKET sock,
  GPIBuffer * outputBuffer,
  GPIBool * connClosed,
  GPIBool clipSentData,
  char id[3]
)
{
	GPIBool closed;
	int sent;
	int total;
	int remaining;
	char * buffer;
	int pos;
	int len;

	assert(outputBuffer != NULL);

	buffer = outputBuffer->buffer;
	len = outputBuffer->len;
	pos = outputBuffer->pos;
	remaining = (len - pos);
	total = 0;

	
	
	if(remaining == 0)
		return GP_NO_ERROR;

	do
	{
		CHECK_RESULT(gpiSendData(connection, sock, &buffer[pos + total], remaining, &closed, &sent, id));
		if(sent)
		{
			total += sent;
			remaining -= sent;
		}
	}
	while(sent && remaining);

	if(clipSentData)
	{
		if(total > 0)
		{
			memmove(buffer, &buffer[total], (unsigned int)remaining + 1);
			len -= total;
		}
	}
	else
	{
		pos += total;
	}

	assert(len >= 0);
	assert(pos >= 0);
	assert(pos <= len);

	
	
	outputBuffer->len = len;
	outputBuffer->pos = pos;
	if(connClosed)
		*connClosed = closed;

	return GP_NO_ERROR;
}
