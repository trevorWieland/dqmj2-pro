#include "context.h"
void native_main_02096258( const u8* seed, u8 * wepkey)
{
	u8 temp[17];
	u8 md5src[3] = {0x61,0x61,0x61};
	MATHMD5Context context;
	MATH_MD5Init( &context );
	MATH_MD5Update( &context, seed, 24);
	MATH_MD5GetHash( &context, temp);
	MI_CpuCopy8( &(temp[3]),wepkey,13);
}
