#include "context.h"
void native_main_020b3b58(GTI2Buffer * buffer, GT2Byte b)
{
	assert(buffer->len < buffer->size);
#if 0
	if(buffer->len >= buffer->size)
		return;
#endif

	buffer->buffer[buffer->len++] = b;
}
