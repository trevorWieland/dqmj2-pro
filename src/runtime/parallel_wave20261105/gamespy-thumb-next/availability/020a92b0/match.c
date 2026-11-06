#include "context.h"
int native_main_020a92b0(const char * hostname, int port, SOCKADDR_IN * saddr)
{
	GS_ASSERT(hostname)
	GS_ASSERT(saddr)

	saddr->sin_family = AF_INET;
	saddr->sin_port = htons((unsigned short)port);
	saddr->sin_addr.s_addr = inet_addr(hostname);
	
	if(saddr->sin_addr.s_addr == INADDR_NONE)
	{
		HOSTENT * host = gethostbyname(hostname);
		if(!host)
			return 0;
		saddr->sin_addr.s_addr = *(unsigned int *)host->h_addr_list[0];
	}

	return 1;
}