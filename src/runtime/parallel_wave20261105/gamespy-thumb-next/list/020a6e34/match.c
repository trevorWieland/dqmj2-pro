#include "context.h"
void native_main_020a6e34(SBServerList *slist, SBServer server)
{
	if (slist->deadlist == NULL)
	{
		native_fn_020a6100(server, NULL);
	} else
		native_fn_020a6100(server, slist->deadlist);
	slist->deadlist = server;	
}