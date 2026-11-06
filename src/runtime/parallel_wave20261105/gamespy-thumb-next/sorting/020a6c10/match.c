#include "context.h"
int GS_STATIC_CALLBACK native_main_020a6c10(const void *entry1, const void *entry2)
{
    SBServer server1 = *(SBServer *)entry1, server2 = *(SBServer *)entry2;
	int diff;
	const char *currsortkey = (const char *)currentSortList->currsortinfo.sortkey;

    diff = native_fn_0201d800(native_fn_020a5fe4(server1, currsortkey, native_data_020e0350),
				native_fn_020a5fe4(server2, currsortkey, native_data_020e0350));

	if (diff == 0) 
		return native_fn_020a69f8(server1, server2);			

	if (!currentSortList->sortascending) 
		diff = -diff;
	return diff;
}