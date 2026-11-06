#include "context.h"
void native_main_020a69b4(ServerBrowser sb, SBBool ascending, const char *sortkey, SBCompareMode comparemode)
{
	SortInfo info;
	info.comparemode = comparemode;
GS_ASSERT(sortkey != NULL);
_tcscpy(info.sortkey,sortkey);
	native_fn_020a6cc0(&sb->list, ascending, info);
}