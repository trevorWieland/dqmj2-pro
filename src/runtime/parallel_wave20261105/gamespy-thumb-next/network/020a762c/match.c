#include "context.h"
void native_main_020a762c(SBServerList *slist)
{
	if (slist->inbuffer != NULL)
		native_fn_020a929c(slist->inbuffer);
	slist->inbuffer = NULL;
	slist->inbufferlen = 0;
	if (slist->slsocket != INVALID_SOCKET)
		native_fn_020a8b6c(slist->slsocket);
	slist->slsocket = INVALID_SOCKET;
	slist->state = sl_disconnected;

	native_fn_020a75ec(slist);
	slist->expectedelements = -1;
	native_fn_020a75b4(slist);	
}