#include "context.h"
u8 native_main_02095aec( ACWORK *wk )
{
	OSTick time = OS_GetTick();
	time = time - wk->timeOut;
	time = OS_TicksToMilliSeconds( time );
	if( time >= SEARCH_STEALTH_TIME_OUT || wk->searchList[ wk->searchListNo ].find == TRUE )
	{
		wk->searchList[ wk->searchListNo ].find = FALSE;
		wk->searchListNo++;
		if( wk->searchListNum <= wk->searchListNo )
		{
			wk->count++;
			wk->searchListNo  = 0;
			wk->searchChannel = DWCi_AC_GetStealthChannel( wk->count );
		}
		if( wk->searchChannel < 0 )
		{
			wk->count = 0;
			return NextSearchCheck( wk, AC_PHASE_SEARCH_STEALTH );
		}
		else
		{
			iScanStartStealth( wk );
		}
	}
 	return AC_PHASE_SEARCH_STEALTH;
}
