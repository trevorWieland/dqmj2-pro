#include "context.h"
int native_main_020b3588(char *buff, int len)
{
	char *pos;
	int oldlen = len;

	pos = FindFinal(buff, len);
	
	while ((len > 0) && (pos != NULL))
	{
		DOXCODE(buff,pos - buff, enc1);
		ProcessStatement(buff, pos - buff);
		len -= (pos - buff) + 7;
		buff = pos + 7; 
		if (len>0)
			pos = FindFinal(buff, len);
	}
	return oldlen - len; 
}
