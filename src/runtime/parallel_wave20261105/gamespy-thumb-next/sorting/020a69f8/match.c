#include "context.h"
int native_main_020a69f8(SBServer server1, SBServer server2)
{
	const char *prevsortkey = (const char *)currentSortList->prevsortinfo.sortkey;
	int diff;
	double f;
	
	switch(currentSortList->prevsortinfo.comparemode)
	{
		case sbcm_int: 
			diff = native_fn_020a601c(server1, prevsortkey, 0) - 
					native_fn_020a601c(server2, prevsortkey, 0);
			break;
		case sbcm_float: 
			f = native_fn_020a6090(server1, prevsortkey, 0) - 
					native_fn_020a6090(server2, prevsortkey, 0);
			if (!currentSortList->sortascending) 
				f = -f;
			if ((float)f > (float)0.0) 
				return 1;
			else if ((float)f < (float)0.0) 
				return -1;
			else
				return 0;
			
		case sbcm_strcase: 
			diff = native_fn_0201d800(native_fn_020a5fe4(server1, prevsortkey, native_data_020e0350),
							native_fn_020a5fe4(server2, prevsortkey, native_data_020e0350));
			break;
		case sbcm_stricase: 
			diff = native_fn_02023f6c(native_fn_020a5fe4(server1, prevsortkey, native_data_020e0350),
								native_fn_020a5fe4(server2, prevsortkey, native_data_020e0350));		
			break;
		default: 
			return 0;		
	}
	if (!currentSortList->sortascending) 
		diff = -diff;
	return diff;
}