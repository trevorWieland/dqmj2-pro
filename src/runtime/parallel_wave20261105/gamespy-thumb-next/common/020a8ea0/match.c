#include "context.h"
char * native_main_020a8ea0(const char *src)
{
	char *res;
	if(src == NULL)      
		return NULL;
	res = (char *)native_fn_020a927c(native_fn_0201d69c(src) + 1);
	if(res != NULL)      
		native_fn_0201d6b8(res, src);
	return res;
}
