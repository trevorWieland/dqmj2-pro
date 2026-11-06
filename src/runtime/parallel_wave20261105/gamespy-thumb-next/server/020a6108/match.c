#include "context.h"
int native_main_020a6108(char *key)
{
	InvalidKeys invalid=native_data_020dc534;
	int i;
	for (i = 0; i < sizeof(invalid.keys)/sizeof(invalid.keys[0]); i++)
	{
		if (native_fn_0201d800(key,invalid.keys[i]) == 0)
			return 0;
	}
	return 1;
}
