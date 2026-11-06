#include "context.h"
void native_main_020a75b4(SBServerList *slist)
{
	int i;
	for (i = 0 ; i < slist->numpopularvalues ; i++)
		native_fn_020a6f78(slist, slist->popularvalues[i]);
	slist->numpopularvalues = 0;
}