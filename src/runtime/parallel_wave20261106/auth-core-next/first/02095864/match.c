#include "context.h"
void native_main_02095864( u8 phase )
{
	ACWORK *wk = DWCi_AC_GetMemPtr( ALLOC_NAME_WORK );
	switch( phase )
	{
	case AC_PHASE_SEARCH_AROUND:
		iScanStartAround( wk );
		break;
	case AC_PHASE_SEARCH_DIFFER_CHANNEL:
		iScanStartDifferChannel( wk );
		break;
	case AC_PHASE_SEARCH_STEALTH:
		iScanStartStealth( wk );
		break;
	}
}
