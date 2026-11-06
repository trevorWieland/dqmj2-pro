#include "context.h"
int native_main_020a7744(char *buf, int len)
{
	int i;
	while (len > 0 && *buf)
	{
		i = native_fn_020a6fa8(buf, len);
		if (i < 0)
			return 0;  
		buf += i;
		len -= i;
		i = native_fn_020a6fa8(buf, len);
		if (i < 0)
			return 0; 
		buf += i;
		len -= i;		
	}
	if (len == 0)
		return 0; 
	if (*buf == 0)
		return 1; 
	return 0;
}