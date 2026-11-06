#include "context.h"
SBError native_main_020a80f8(SBServerList *slist, char *buf, int len)
{

	SBServer server;
	goa_uint32 ip;
	unsigned short port;
	int foundexisting;
	int i;

	if (len < 5)
		return sbe_dataerror;
	
	native_fn_020a7814(slist, buf, len, &ip, &port);
	
	foundexisting = native_fn_020a6de4(slist, ip, port);
	if (foundexisting == -1) 
	{
		server = native_fn_020a64d4(slist, ip, port);
		if (native_fn_020a6550(server))
			return sbe_allocerror;
	} else
		server = native_fn_020a6e9c(slist, foundexisting);
	i = native_fn_020a7858(slist, server, buf, len, 0);
	if (i < 0)
		return sbe_dataerror; 
	if (foundexisting == -1)
		native_fn_020a6d84(slist, server);
	slist->ListCallback(slist, slc_serverupdated, server, slist->instance);
	return sbe_noerror;
	
}