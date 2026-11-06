#include "context.h"
void native_main_020a7260(char **buffer, int ival, int *len)
{
	memcpy(*buffer, &ival, 4);
	(*len) += 4;
	(*buffer) += 4;
}