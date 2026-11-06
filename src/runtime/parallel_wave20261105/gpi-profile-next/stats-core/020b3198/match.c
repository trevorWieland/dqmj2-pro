#include "context.h"
void native_main_020b3198(char *buf, int len)
{
	int i;
	char *pos = enc;

	for (i = 0 ; i < len ; i++)
	{
		buf[i] ^= *pos++;
		if (*pos == 0)
			pos = enc;
	}
}
