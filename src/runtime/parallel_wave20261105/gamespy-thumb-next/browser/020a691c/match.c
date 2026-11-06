#include "context.h"
void native_main_020a691c(ServerBrowser sb, SBServer server)
{
	int i = native_fn_020a6db0(&sb->list, server);
	if (i != -1)
		native_fn_020a6e5c(&sb->list, i);
}