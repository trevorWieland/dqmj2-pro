#include "context.h"
GT2Bool native_main_020b3b0c
(
	const GT2Byte * response1,
	const GT2Byte * response2
)
{
	int i; 
	for (i = 0 ; i < GTI2_RESPONSE_LEN ; i++)
	{
		if (i != 0 && i != 13 && response1[i] != response2[i])
			return GT2False;
	}
	return GT2True;
}
