#include "context.h"
int native_main_020a6db0(SBServerList *slist, SBServer findserver)
{
	int numservers;
	int i;
	numservers = native_fn_020a8640(slist->servers);
	for (i = 0 ; i < numservers ; i++)
	{
		if (findserver == *(SBServer *)native_fn_020a8644(slist->servers, i))
		{
			return i;
		}
	}
	return -1;
}