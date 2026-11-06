#include "context.h"
int GS_STATIC_CALLBACK native_main_020a6b5c(const void *entry1, const void *entry2)
{
    SBServer server1 = *(SBServer *)entry1, server2 = *(SBServer *)entry2;
	double f;
	const char *currsortkey = (const char *)currentSortList->currsortinfo.sortkey;

	f = native_fn_020a6090(server1, currsortkey, 0) - 
			native_fn_020a6090(server2, currsortkey, 0);

	
	if ( !((float)f > (float)0.0) && !((float)f < (float)0.0) )
		return native_fn_020a69f8(server1, server2);			

	if (!currentSortList->sortascending) 
		f = -f;
	if ((float)f > (float)0.0) 
		return 1;
	else if ((float)f < (float)0.0) 
		return -1; 
	else 
		return 0;
}