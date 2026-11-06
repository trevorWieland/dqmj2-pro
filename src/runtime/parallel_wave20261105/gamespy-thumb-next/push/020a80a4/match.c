#include "context.h"
SBError native_main_020a80a4(SBServerList *slist, char *buf, int len)
{
	goa_uint32 ip;
	unsigned short port;
	int i;

	if (len < 6)
		return sbe_dataerror;
	
	memcpy(&ip, buf, 4);
	memcpy(&port, buf + 4, 2);
	
	i = native_fn_020a6de4(slist, ip, port);
	if (i == -1)
		return sbe_noerror;
	native_fn_020a6e5c(slist, i);
	return sbe_noerror;
}