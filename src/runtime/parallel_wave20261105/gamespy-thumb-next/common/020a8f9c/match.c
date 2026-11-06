#include "context.h"
void native_main_020a8f9c(char *quart, char *trip, int inlen)
{
	if (inlen >= 2)
		trip[0] = (char)(quart[0] << 2 | quart[1] >> 4);
	if (inlen >= 3)
		trip[1] = (char)((quart[1] & 0x0F) << 4 | quart[2] >> 2);
	if (inlen >= 4)
		trip[2] = (char)((quart[2] & 0x3) << 6 | quart[3]);
}
