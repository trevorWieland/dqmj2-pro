#include "context.h"
void native_main_020a6d84(SBServerList *slist, SBServer server)
{
	native_fn_020a865c(slist->servers, &server);
	slist->ListCallback(slist, slc_serveradded, server, slist->instance);
}