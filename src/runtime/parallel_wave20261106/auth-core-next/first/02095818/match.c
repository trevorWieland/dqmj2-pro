#include "context.h"
s8 native_main_02095818( u16 no )
{
	ACWORK *wk = DWCi_AC_GetMemPtr( ALLOC_NAME_WORK );
	u8  i,j;
	u16 channel = wk->stealthChannel;
	if( channel == 0 ) return -1;
	for( i = 0, j = 0 ; i < 13 ; i++ )
	{
		if(( channel & ( 1 << i )) != FALSE )
		{
			if( j == no ) return (s8)i;
			j++;
		}
	}
	return -1;
}
