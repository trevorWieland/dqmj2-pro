#include "context.h"
void native_main_020a6cc0(SBServerList *slist, SBBool ascending, SortInfo sortinfo)
{
	ArrayCompareFn comparator;
	switch (sortinfo.comparemode)
	{
	case sbcm_int: comparator = native_fn_020a6b10;
		break;
	case sbcm_float: comparator = native_fn_020a6b5c;
		break;
	case sbcm_strcase: comparator = native_fn_020a6c10;
		break;
	case sbcm_stricase: comparator = native_fn_020a6c68;
		break;
	default: 
		comparator = native_fn_020a6c68;
	}

	
	if (_tcslen(slist->prevsortinfo.sortkey) == 0) 
		slist->prevsortinfo = sortinfo;
	else if (native_fn_0201d800((const char *)sortinfo.sortkey, (const char *)slist->currsortinfo.sortkey) != 0)
		slist->prevsortinfo = slist->currsortinfo; 
	
	slist->currsortinfo = sortinfo;
	slist->sortascending = ascending;
	currentSortList = slist;
	native_fn_020a8750(slist->servers,comparator);
}