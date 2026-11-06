#include "context.h"
int native_main_020a6de4(SBServerList *slist, goa_uint32 ip, unsigned short port)
{
	int numservers;
	SBServer server;
	int i;
	numservers = native_fn_020a8640(slist->servers);
	for (i = 0 ; i < numservers ; i++)
	{
		server = *(SBServer *)native_fn_020a8644(slist->servers, i);
		if (native_fn_020a60b0(server) == ip && native_fn_020a60cc(server) == port)
		{
			return i;
		}
	}
	return -1;
}