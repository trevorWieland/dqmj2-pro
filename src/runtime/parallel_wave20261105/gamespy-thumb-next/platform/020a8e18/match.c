#include "context.h"
int native_main_020a8e18(IN_ADDR * addr)
{
	int b1;
	int b2;
	unsigned int ip;

	
	ip = ntohl(addr->s_addr);
	b1 = (int)((ip >> 24) & 0xFF);
	b2 = (int)((ip >> 16) & 0xFF);

	
	if(b1 == 10)
		return 1;

	
	if((b1 == 172) && ((b2 >= 16) && (b2 <= 31)))
		return 1;

	
	if((b1 == 192) && (b2 == 168))
		return 1;

	return 0;
}