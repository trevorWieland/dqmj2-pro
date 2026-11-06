#include "context.h"
int native_main_020a6fa8(char *buf,int len)
{
	int i;
	for (i = 0 ; i < len ; i++)
	{
		if (buf[i] == '\0') 
			return i + 1; 
	}
	return -1;
}
