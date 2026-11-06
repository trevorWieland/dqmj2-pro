#include "context.h"
int GS_STATIC_CALLBACK native_main_020b5984(const void * elem1, const void * elem2)
{
	GT2Connection connection1 = *(GT2Connection *)elem1;
	GT2Connection connection2 = *(GT2Connection *)elem2;
	if(connection1->ip != connection2->ip)
		return (int)(connection1->ip - connection2->ip);
	return (int)(short)(connection1->port - connection2->port);
}
