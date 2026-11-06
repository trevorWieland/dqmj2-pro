#include "context.h"
GPResult
native_main_020acb98(
  GPConnection * connection,
  GPIBuffer * buffer
)
{
	if(!buffer || !buffer->buffer || !buffer->pos)
		return GP_NO_ERROR;

	buffer->len -= buffer->pos;
	if(buffer->len)
		memmove(buffer->buffer, buffer->buffer + buffer->pos, (unsigned int)buffer->len);
	buffer->buffer[buffer->len] = '\0';
	buffer->pos = 0;

	GSI_UNUSED(connection);
	return GP_NO_ERROR;
}
