#include "context.h"
void native_main_02096288( const u8* seed, u8 * wepkey)
{
	int i;
	u8 keytemp[ WEPKEY_LENGTH ];
	for( i = 0 ; i < WEPKEY_LENGTH ; i++ )
	{
			wepkey[i] = (u8)(seed[i] ^ seed[WEPKEY_LENGTH + i % 7]);
	}
	for( i = 0 ; i < 7 ; i++ )
	{
		wepkey[3 + i] = (u8)(wepkey[3 + i] ^ seed[WEPKEY_LENGTH + i]);
	}
	for( i = 0 ; i < WEPKEY_LENGTH ; i++ )
	{
		wepkey[i] = (u8)(wepkey[i] ^ MASKkey0[i]);
	}
	MI_CpuCopy8( wepkey, keytemp, WEPKEY_LENGTH );
	for( i = 0 ; i < WEPKEY_LENGTH ; i++ )
	{
		wepkey[CONV_BYTE_TABLE[i]]=keytemp[i];
	}
	for ( i = 0 ; i < WEPKEY_LENGTH ; i++ )
	{
		wepkey[i] = (u8)(wepkey[i] ^ MASKkey1[i]);
	}
	for ( i = 0 ; i < WEPKEY_LENGTH ; i++ )
	{
		wepkey[i] = (u8)(CONV_4BIT_TABLE[(wepkey[i] >> 4) & 0x0F] << 4 | CONV_4BIT_TABLE[wepkey[i] & 0x0F] );
	}
	for( i = 0 ; i < 3 ; i++ )
	{
		wepkey[i]     = (u8)(wepkey[i]     ^ wepkey[i + 6]);
		wepkey[i + 3] = (u8)(wepkey[i + 3] ^ wepkey[i + 9]);
		wepkey[i + 6] = (u8)(wepkey[i + 6] ^ wepkey[i + 3]);
		wepkey[i + 9] = (u8)(wepkey[i + 9] ^ wepkey[i]);
		wepkey[12]    = (u8)(wepkey[12]    ^ wepkey[i]);
	}
}
