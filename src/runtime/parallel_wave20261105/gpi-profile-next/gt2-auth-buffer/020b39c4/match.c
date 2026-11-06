#include "context.h"
GT2Byte * native_main_020b39c4
(
	GT2Byte * buffer
)
{
	int i;
	int oddmode;
	assert(buffer);

	srand((unsigned int)current_time());
	buffer[0] = (GT2Byte)(33 + rand() % 93); 
	oddmode = 0;
	for (i = 1; i < GTI2_CHALLENGE_LEN ; i++)
	{
		oddmode = CALCULATEODDMODE(buffer,i, oddmode);
		buffer[i] = (GT2Byte)(33 + rand() % 93); 
		
		if ((oddmode && (buffer[i] & 1) == 0) || (!oddmode && ((buffer[i] & 1) == 1)))
			buffer[i]++;

	}
	return buffer;
}
