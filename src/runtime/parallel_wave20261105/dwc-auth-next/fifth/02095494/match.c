#include "context.h"
u32 native_main_02095494(tagACWORK * wk)
{
	u8   num   = 0;
	ACSL *list = wk->searchList;

	num = native_fn_0209557c( wk );
	list += num;

	if( wk->connectType == 0 || wk->connectType == DWC_AC_AP_TYPE_FREESPOT + 1 )
	{
		MI_CpuCopy8( FREESPOT_SSID, list->ssid, FREESPOT_SSID_LENGTH );
		list->length = FREESPOT_SSID_LENGTH;
		list->type   = AP_TYPE_FREESPOT;
		num++;
	}

	return num;
}
