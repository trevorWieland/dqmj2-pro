#include "context.h"
void native_main_020a6f78(SBServerList *slist, const char *str)
{
	SBRefString ref, *val;
	ref.str = str;
	val = (SBRefString *)native_fn_020a8a3c(native_fn_020a5f1c(slist), &ref);
	assert(val != NULL);
	if (val == NULL)
		return; 
	val->refcount--;
	if (val->refcount == 0)
		native_fn_020a89f0(native_fn_020a5f1c(slist), &ref);
}