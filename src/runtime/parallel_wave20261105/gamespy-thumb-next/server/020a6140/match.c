#include "context.h"
char *native_main_020a6140(char *instr, char delim)
{
	char *result;
	
	
	if (instr)
		native_data_021d2360 = instr;
	result=native_data_021d2360;
	while (*native_data_021d2360 && *native_data_021d2360 != delim)
	{
		native_data_021d2360++;
	}
	if (native_data_021d2360 == result)
		result = NULL;
	if (*native_data_021d2360) 
		*native_data_021d2360++ = '\0';
	return result;
}
