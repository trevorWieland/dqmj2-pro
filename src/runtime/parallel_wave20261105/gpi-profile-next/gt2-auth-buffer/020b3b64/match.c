#include "context.h"
void native_main_020b3b64(GTI2Buffer * buffer, unsigned short s)
{
	assert((buffer->len + 2) <= buffer->size);
#if 0
	if((buffer->len + 2) > buffer->size)
		return;
#endif

	buffer->buffer[buffer->len++] = (GT2Byte)((s >> 8) & 0xFF);
	buffer->buffer[buffer->len++] = (GT2Byte)(s & 0xFF);
}
