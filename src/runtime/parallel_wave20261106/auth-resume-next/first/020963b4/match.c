#include "context.h"
int native_main_020963b4( const char *src, u8 *dest, u32 srcsize, u32 destsize )
{
	U4B u4b;
	u32 x;
	u32 base64 = 0;
	int srcmod = 0;
	int srcmax = 0;
	int i,j,k;
	if( destsize >= ( srcsize * 3 ) / 4 ){
		srcmod = (int)(srcsize % 4);
		srcmax = (int)(srcsize - srcmod);
	}else{
		return -1;
	}
	for (i=0; i<srcmax;i+=4){
		base64 = 0;
		for(j=0; j < 4;j++){
			x = (u32)codetovalue((u8)src[i+j]);
			base64 |= x << ( 3 - j )*6;
		}
		u4b.us32 = base64;
		for(k=0; k < 3; k++ ){
			dest[ (i/4)*3 + k ] = u4b.us8[ 2 - k ];
		}
	}
	if( srcmod ) {
		u4b.us32=0;
		base64 = 0;
		for ( i = 0 ; i < srcmod; i++)
		{
			x = (u32)codetovalue((u8)src[ srcmax + i ]);
			base64 |= x << ( 3 - i )*6;
			u4b.us32 = u4b.us32 | base64;
		}
		for( k=0; k < srcmod; k++ ){
			dest[ (srcmax*3)/4 + k ] = u4b.us8[ 2 - k ];
		}
	}
	return (int)(( srcsize * 3 ) / 4 );
}
