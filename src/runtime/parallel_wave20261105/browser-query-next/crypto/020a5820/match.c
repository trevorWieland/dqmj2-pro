#include "context.h"
void native_main_020a5820(GOACryptState *state, unsigned char *bp, int len)
{
	int i;
	for (i = 0 ; i < len ; i++)
	{
		bp[i] = GOADecryptByte(state, bp[i]);
	}
}