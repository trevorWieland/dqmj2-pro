#include "context.h"
u8 native_main_020959d0( ACWORK *wk )
{
	wk->count = 0;
	wk->aroundCount++;
    (void)DWCi_AC_MakeSearchList( SEARCH_LIST_AROUND );
	wk->searchChannel = DWC_AC_SEARCH_START_CHANNEL2;
	return AC_PHASE_SEARCH_AROUND;
}
