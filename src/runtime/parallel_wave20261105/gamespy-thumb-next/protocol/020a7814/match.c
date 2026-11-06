#include "context.h"
void native_main_020a7814(SBServerList *slist, char *buf, int len, goa_uint32 *ip, unsigned short *port)
{
	unsigned char flags;
	if (len < 5)
		return; 
	flags = (unsigned char)buf[0];
	buf++;
	len--;
	memcpy(ip, buf, 4);
	
	buf += 4;
	len -= 4;
		
	if (flags & NONSTANDARD_PORT_FLAG)
	{
		if (len < 2)
			return; 
		memcpy(port, buf, 2);
	} else
		*port = slist->defaultport;
}