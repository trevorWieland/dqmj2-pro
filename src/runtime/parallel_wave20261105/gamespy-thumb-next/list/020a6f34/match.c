#include "context.h"
const char *native_main_020a6f34(SBServerList *slist, const char *str)
{
	SBRefString ref, *val;
	ref.str = str;
	val = (SBRefString *)native_fn_020a8a3c(native_fn_020a5f1c(slist), &ref);
	if (val != NULL)
	{
		val->refcount++;
		return val->str;
	}

	
	ref.str = native_fn_020a8ea0(str);
	ref.refcount = 1;
#ifdef GSI_UNICODE
	ref.str_W = UTF8ToUCS2StringAlloc(str);
#endif
	native_fn_020a89a4(native_fn_020a5f1c(slist), &ref);
	return ref.str;
	
	
}