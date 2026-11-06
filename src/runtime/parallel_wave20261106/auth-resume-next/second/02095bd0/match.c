#include "context.h"
u8 native_main_02095bd0( ACWORK *wk, u8 phase )
{
	switch( phase )
	{
	case AC_PHASE_SEARCH_AROUND:
		if( wk->findListNum != 0 || wk->stealthChannel != 0 )
		{
			if( DWCi_AC_MakeSearchList( SEARCH_LIST_DIFFER_CHANNEL ) != 0 )
			{
				phase = AC_PHASE_SEARCH_DIFFER_CHANNEL;
			}
			else
			{
				phase = CheckStartStealthSearch( wk );
			}
		}
		else
		{
			if( wk->aroundCount < AROUND_SEARCH_NUM_MAX )
			{
				phase = SearchAround2ndLap( wk );
			}
			else
			{
				phase = AC_PHASE_SEARCH_END;
			}
		}
		break;
	case AC_PHASE_SEARCH_DIFFER_CHANNEL:
		phase = CheckStartStealthSearch( wk );
		break;
	case AC_PHASE_SEARCH_STEALTH:
		if( wk->aroundCount < AROUND_SEARCH_NUM_MAX )
		{
			phase = SearchAround2ndLap( wk );
		}
		else
		{
			phase = AC_PHASE_SEARCH_END;
		}
		break;
	default:
		break;
	}
	DWCi_AC_SearchReStart( phase );
	return phase;
}
