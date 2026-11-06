#include "context.h"
void native_main_020b76bc ( uchar *ins, int size, uchar *result )
{
	int    i,pos;
	uchar  trip[3];
	uchar  kwart[4];
	i=0;
	while (i < size)
	{
		for (pos=0 ; pos <= 2 ; pos++, i++)
			if (i < size) trip[pos] = *ins++;
			else trip[pos] = '\0';
			kwart[0] = (unsigned char)(  (trip[0])       >> 2);
			kwart[1] = (unsigned char)((((trip[0]) &  3) << 4) + ((trip[1]) >> 4));
			kwart[2] = (unsigned char)((((trip[1]) & 15) << 2) + ((trip[2]) >> 6));
			kwart[3] = (unsigned char)(  (trip[2]) & 63);
			for (pos=0; pos <= 3; pos++) *result++ = native_fn_020b7684(kwart[pos]);
	}
	*result='\0';
}
