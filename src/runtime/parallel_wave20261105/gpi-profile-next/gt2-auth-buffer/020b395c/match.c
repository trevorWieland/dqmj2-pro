#include "context.h"
int native_main_020b395c(const GT2Byte *buffer)
{
	int oddmode = 0;
	int i;
	for (i = 1; i < GTI2_CHALLENGE_LEN ; i++)
	{
		oddmode = CALCULATEODDMODE(buffer,i, oddmode);
		if ((oddmode && (buffer[i] & 1) == 0) || (!oddmode && ((buffer[i] & 1) == 1)))
			return 0; 
	}
	return 1;
}
