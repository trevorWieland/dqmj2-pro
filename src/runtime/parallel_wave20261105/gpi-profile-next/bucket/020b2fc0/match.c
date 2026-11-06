#include "context.h"
char *native_main_020b2fc0(char *s)
{
	char *p = s;
	while (*s)
	{
		if (*s == '\\')
			*s = '/';
		s++;
	}
	return p;
}
