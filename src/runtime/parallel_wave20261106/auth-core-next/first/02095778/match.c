#include "context.h"
u8 native_main_02095778( void )
{
	ACWORK     *wk       = DWCi_AC_GetMemPtr( ALLOC_NAME_WORK );
	u8         dwc_phase = DWCi_AC_GetPhase();
	int        wcm_phase = WCM_GetPhase();
	if( dwc_phase == AC_PHASE_SEARCH_START && wcm_phase == WCM_PHASE_IDLE )
	{
		dwc_phase = SearchStart( wk );
	}
	else if( dwc_phase == AC_PHASE_SEARCH_END )
	{
		dwc_phase = SearchEndCheck( wk, dwc_phase );
	}
	else if( wcm_phase == WCM_PHASE_IDLE || wcm_phase == WCM_PHASE_SEARCH )
	{
		dwc_phase = SearchEndCheck( wk, dwc_phase );
		if( dwc_phase != AC_PHASE_CONNECT_START )
		{
			if     ( dwc_phase == AC_PHASE_SEARCH_AROUND )         dwc_phase = SearchAround( wk );
			else if( dwc_phase == AC_PHASE_SEARCH_DIFFER_CHANNEL ) dwc_phase = SearchDifferChannel( wk );
			else if( dwc_phase == AC_PHASE_SEARCH_STEALTH )        dwc_phase = SearchStealth( wk );
		}
	}
	return dwc_phase;
}
