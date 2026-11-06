#include "context.h"
SBError native_main_020a8480(SBServerList *slist)
{
	char indata[1500];  
	struct   sockaddr_in saddr;
	int saddrlen = sizeof(saddr);
	int error;
	int foundexisting;
	SBServer server;

	while (native_fn_020a8d88(slist->slsocket)) 
	{
#if defined(_PS3)
		error = (int)native_fn_020a8c00(slist->slsocket, indata, sizeof(indata) - 1, 0, (struct sockaddr *)&saddr, (socklen_t*)&saddrlen );
#else
		error = (int)native_fn_020a8c00(slist->slsocket, indata, sizeof(indata) - 1, 0, (struct sockaddr *)&saddr, &saddrlen );
#endif

		if (gsiSocketIsError(error))
			continue; 
		
		foundexisting = native_fn_020a6de4(slist, saddr.sin_addr.s_addr, saddr.sin_port);
		if (foundexisting != -1) 
			continue;
		server = native_fn_020a64d4(slist, saddr.sin_addr.s_addr, saddr.sin_port);
		if (native_fn_020a6550(server))
			return sbe_allocerror;
		native_fn_020a6538(server, UNSOLICITED_UDP_FLAG|NONSTANDARD_PORT_FLAG);
		native_fn_020a6d84(slist, server);
	}
	if (native_fn_020a8ef8() - slist->lanstarttime > SL_LAN_SEARCH_TIME) 
	{
		native_fn_020a8b6c(slist->slsocket);
		slist->slsocket = INVALID_SOCKET;
		slist->state = sl_disconnected;
		slist->ListCallback(slist, slc_initiallistcomplete, SBNullServer, slist->instance);
	}
	return sbe_noerror;
}