#include "context.h"
int native_main_020a6454(const char *s, int numbuckets)
{
	goa_uint32 hashcode = 0;
	while (*s != 0)
	{
		hashcode = (goa_uint32)((int)hashcode * MULTIPLIER + lower(*s));
		s++;
	}
    return (int)(hashcode % numbuckets);

}
