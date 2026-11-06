#include "context.h"
u8 native_main_02095910( ACWORK *wk )
{
	wk->timeOut       = OS_GetTick();
	wk->searchChannel = DWC_AC_SEARCH_START_CHANNEL1;
	iScanStartAround( wk );
	return AC_PHASE_SEARCH_AROUND;
}
