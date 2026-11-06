#include "context.h"
SBError native_main_020a855c(SBServerList *slist)
{
	native_fn_020a6ea8(slist); 
	switch (slist->state)
	{
	case sl_disconnected:
		break;
	case sl_connected:
	case sl_mainlist:
		return native_fn_020a82a0(slist);
		
	case sl_lanbrowse:
		return native_fn_020a8480(slist);
		
	}

	return sbe_noerror;
	
	
}