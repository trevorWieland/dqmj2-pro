#include "context.h"
static inline BOOL iCopySSID(int no,DWCMemPage *info,ACSL *list,int base_type)
{
	u8 j;
	for( j = 0 ; j < WM_SIZE_SSID ; j++ )
	{
		if( info->ap.ssid[ no ][ j ] == 0 ) break;
		list->ssid[ j ] = info->ap.ssid[ no ][ j ];
	}
	if( j != 0)
	{
		list->length = j;
		list->type   = (u8)base_type;
		return TRUE;
	}
	return FALSE;
}

u8 native_main_0209557c( tagACWORK *wk )
{
	int        i;
	u8         num   = 0;
	DWCMemPage *info = wk->userInfo;
	ACSL       *list = wk->searchList;

	for( i = 0 ; i < 3 ; i++ )
	{

		if( wk->connectType == 0 || wk->connectType == DWC_AC_AP_TYPE_USER1 + 1 + i )
		{
			if( info->ap.setType != 0xFF )
			{
				if( iCopySSID( SSID_NO_USER_NORMAL, info, list, AP_TYPE_USER1 + i ) != FALSE )
				{
					num++;
					list++;
				}
				if( info->ap.setType == 1 )
				{
					if( iCopySSID( SSID_NO_USER_AOSS, info, list, AP_TYPE_AOSS_USER1 + i ) != FALSE )
					{
						num++;
						list++;
					}
				}
			}
		}
		info++;
	}
	return num;
}
