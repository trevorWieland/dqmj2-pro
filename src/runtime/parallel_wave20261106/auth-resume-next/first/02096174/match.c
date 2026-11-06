#include "context.h"
void native_main_02096174( const char *ssid, u8 pos[10] )
{
	u8 buf[24];
	decodeSSID( ssid, buf );
	if ( !memcmp( buf, NINTENDO_SHOP_SSID, NINTENDO_SHOP_SSID_LENGTH ))
	{
		MI_CpuCopy8( (u8 *)&buf[ NINTENDO_SHOP_SSID_LENGTH ], pos, 10 );
	}
}
