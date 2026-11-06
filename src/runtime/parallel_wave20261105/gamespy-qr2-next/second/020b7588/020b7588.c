#include "context.h"
gsi_bool native_main_020b7588(qr2_buffer_t outbuf, const char *value)
{
	GS_ASSERT(outbuf)
	GS_ASSERT(value)
	{
		int copylen;
		copylen = (int)native_fn_0201d69c(value) + 1;
		if (copylen > AVAILABLE_BUFFER_LEN(outbuf))
			copylen = AVAILABLE_BUFFER_LEN(outbuf);
		if (copylen <= 0)
			return gsi_false;
		native_fn_0201b19c(outbuf->buffer + outbuf->len, value, (unsigned int)copylen);
		outbuf->len += copylen;
		outbuf->buffer[outbuf->len - 1] = 0;
		return gsi_true;
	}
}
