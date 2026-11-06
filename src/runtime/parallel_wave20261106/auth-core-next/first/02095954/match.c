#include "context.h"
u8 native_main_02095954( ACWORK *wk )
{
	OSTick time = OS_GetTick();
	time = time - wk->timeOut;
	time = OS_TicksToMilliSeconds( time );
	if( time >= SEARCH_AROUND_TIME_OUT )
	{
		wk->searchChannel += 2;
		if( wk->searchChannel >= 13 )
		{
			return NextSearchCheck( wk, AC_PHASE_SEARCH_AROUND );
		}
		else
		{
			iScanStartAround( wk );
		}
	}
	return AC_PHASE_SEARCH_AROUND;
}
