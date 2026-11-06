#include "context.h"
void native_main_020b7740 ( uchar *key, int key_len, uchar *buffer_ptr, int buffer_len )
{
	short counter;
	uchar x, y, xorIndex;
	uchar state[256];
	for ( counter = 0; counter < 256; counter++) state[counter] = (uchar) counter;
	x = 0; y = 0;
	for ( counter = 0; counter < 256; counter++)
	{
		y = (uchar)((key[x] + state[counter] + y) % 256);
		x = (uchar)((x + 1) % key_len);
		native_fn_020b7678 ( &state[counter], &state[y] );
	}
	x = 0; y = 0;
	for ( counter = 0; counter < buffer_len; counter ++)
	{
		x = (uchar)((x + buffer_ptr[counter] + 1) % 256);
		y = (uchar)((state[x] + y) % 256);
		native_fn_020b7678 ( &state[x], &state[y] );
		xorIndex = (uchar)((state[x] + state[y]) % 256);
		buffer_ptr[counter] ^= state[xorIndex];
	}
}
