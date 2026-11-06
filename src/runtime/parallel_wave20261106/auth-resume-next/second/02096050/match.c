#include "context.h"
uint native_main_02096050(byte *add)
{
	u32 address = 0;
	address |= ( *add ) << 24;
	add++;
	address |= ( *add ) << 16;
	add++;
	address |= ( *add ) << 8;
	add++;
	address |= *add;
	return SOC_HtoNl( address );
}
