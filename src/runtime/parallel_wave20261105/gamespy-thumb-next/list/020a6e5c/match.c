#include "context.h"
void native_main_020a6e5c(SBServerList *slist, int index)
{
	SBServer server = *(SBServer *)native_fn_020a8644(slist->servers, index);
	slist->ListCallback(slist, slc_serverdeleted, server, slist->instance);
	
	native_fn_020a8720(slist->servers, index);
	
	native_fn_020a6e34(slist, server);
}