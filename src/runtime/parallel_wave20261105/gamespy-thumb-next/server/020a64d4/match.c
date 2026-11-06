#include "context.h"
SBServer native_main_020a64d4(SBServerList *slist, goa_uint32 publicip, unsigned short publicport)
{
	SBServer server;
	server = (SBServer)native_fn_020a927c(sizeof(Server));
	if (server == NULL)
		return NULL;
	server->keyvals = native_fn_020a88ec(sizeof(SBKeyValuePair),NUM_BUCKETS,NUM_CHAINS, native_fn_020a64ac, native_fn_020a64b8, native_fn_020a6494);
	if (server->keyvals == NULL)
	{
		native_fn_020a929c(server);
		return NULL;
	}
	server->state = 0;
	server->flags = 0;
	server->next = NULL;
	server->updatetime = 0;
	server->icmpip = 0;
	server->publicip = publicip;
	server->publicport = publicport;
	server->privateip = 0;
	server->privateport = 0;

	GSI_UNUSED(slist);
	return server;	
}
