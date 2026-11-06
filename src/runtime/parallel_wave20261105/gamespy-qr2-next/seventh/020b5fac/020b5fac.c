#include "context.h"
GT2Bool native_main_020b5fac(const char * string, unsigned int * ip, unsigned short * port)
{
	unsigned int srcIP		= 0;
	unsigned short srcPort	= 0;
	if(!string || !string[0])
	{
		srcIP = 0;
		srcPort = 0;
	}
	else
	{
		char stackHost[GTI2_STACK_HOSTLEN_MAX + 1];
		const char * colon;
		const char * host;
		colon = native_fn_0201d948(string, ':');
		if(!colon)
		{
			host = string;
			srcPort = 0;
		}
		else
		{
			int len;
			const char * check;
			int temp;
			if(colon == string)
			{
				host = NULL;
				srcIP = 0;
			}
			else
			{
				len = (colon - string);
				assert(len < GTI2_STACK_HOSTLEN_MAX);
				native_fn_0201b19c(stackHost, string, (unsigned int)len);
				stackHost[len] = '\0';
				host = stackHost;
			}
			for(check = (colon + 1) ; *check ; check++)
				if(!isdigit(*check))
					return GT2False;
			temp = native_fn_0201f274(colon + 1);
			if((temp < 0) || (temp > 0xFFFF))
				return GT2False;
			srcPort = (unsigned short)temp;
		}
		if(host)
		{
			srcIP = native_fn_020a8c84(host);
			if(srcIP == INADDR_NONE)
			{
#if defined(_XBOX)
				return GT2False;
#else
				HOSTENT * hostent;
				hostent = native_fn_0209046c(host);
				if(hostent == NULL)
					return GT2False;
				srcIP = *(unsigned int *)hostent->h_addr_list[0];
#endif
			}
		}
	}
	if(ip)
		*ip = srcIP;
	if(port)
		*port = srcPort;
	return GT2True;
}
