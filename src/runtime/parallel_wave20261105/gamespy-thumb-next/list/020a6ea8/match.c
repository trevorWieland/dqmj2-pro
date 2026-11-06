#include "context.h"
void native_main_020a6ea8(SBServerList *slist)
{
	SBServer server, next;
	if (slist->deadlist == NULL)
		return;
	server = slist->deadlist;
	while (server != NULL)
	{
		next = native_fn_020a6104(server);
		native_fn_020a5f80(&server);
		server = next;
	}
	slist->deadlist = NULL;
}