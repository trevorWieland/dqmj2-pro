#include "context.h"
void native_main_020a728c(char **buffer, int ival, int *len)
{
	unsigned int ivalNBO = htonl(ival);
	unsigned int ivalBE = 0;
	ivalBE |= ((0x000000FF&ivalNBO)<<24);
	ivalBE |= ((0x0000FF00&ivalNBO)<< 8);
	ivalBE |= ((0x00FF0000&ivalNBO)>> 8);
	ivalBE |= ((0xFF000000&ivalNBO)>>24);
	native_fn_020a7260(buffer, (int)ivalBE, len); 		
}