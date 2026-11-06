#include "context.h"
u8 native_main_020954dc( tagACWORK *wk )
{
	u8   num   = 0;
	ACSL *list = wk->searchList;

	num = native_fn_0209557c( wk );
	list += num;

	if( wk->connectType == 0 || wk->connectType == DWC_AC_AP_TYPE_USB + 1 )
	{
		MI_CpuCopy8( NINTENDO_USB_SSID, list->ssid, NINTENDO_USB_SSID_LENGTH );
		list->length = NINTENDO_USB_SSID_LENGTH;
		list->type   = AP_TYPE_USB;
		num++;
		list++;
	}

	if( wk->connectType == 0 || wk->connectType == DWC_AC_AP_TYPE_WAYPORT + 1 )
	{
		MI_CpuCopy8( WAYPORT_SSID, list->ssid, WAYPORT_SSID_LENGTH );
		list->length = WAYPORT_SSID_LENGTH;
		list->type   = AP_TYPE_WAYPORT;
		num++;
		list++;
	}

	if( wk->connectType == 0 || wk->connectType == DWC_AC_AP_TYPE_NINTENDOWFC + 1 )
	{
		MI_CpuCopy8( NINTENDOWFC_SSID, list->ssid, NINTENDOWFC_SSID_LENGTH );
		list->length = NINTENDOWFC_SSID_LENGTH;
		list->type   = AP_TYPE_NINTENDOWFC;
		num++;
	}

	return num;
}
