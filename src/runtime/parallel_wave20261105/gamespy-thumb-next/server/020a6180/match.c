#include "context.h"
void native_main_020a6180(SBServer server, char *keyvals)
{
	char *k, *v;
	
	k = native_fn_020a6140(++keyvals,'\\'); 
	while (k != NULL)
	{
		v = native_fn_020a6140(NULL,'\\');
		if (v == NULL)
			v = native_data_020e0320;
		if (native_fn_020a6108(k))
		{
			
			if (!native_fn_020b85a8(k))
			{
				native_fn_020a5f98(server, k, v);
			}	
		}
		k = native_fn_020a6140(NULL,'\\');		
	}
}
