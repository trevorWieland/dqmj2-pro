#include "context.h"
char *native_main_020b326c(char *buff, int len)
{
	char *pos = buff;
	
	while (pos - buff < len - 6)
	{
		if (pos[0] == '\\' && 
			pos[1] == 'f'  && 
			pos[2] == 'i'  && 
			pos[3] == 'n'  && 
			pos[4] == 'a'  && 
			pos[5] == 'l'  && 
			pos[6] == '\\')
		{
			return pos;
		} else
			pos++;
	}
	return NULL;	
}
