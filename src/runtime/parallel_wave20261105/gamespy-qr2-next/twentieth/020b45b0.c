#include "context.h"
unsigned short native_main_020b45b0(const GT2Byte * buffer, int pos)
{
	unsigned short s;
	s = (unsigned short)((buffer[pos] << 8) & 0xFF00);
	pos++;
	s |= buffer[pos];
	return s;
}
