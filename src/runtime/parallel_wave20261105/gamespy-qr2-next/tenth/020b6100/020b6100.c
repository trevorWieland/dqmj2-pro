#include "context.h"
unsigned short native_main_020b6100(SOCKET sock)
{
	int ret;
	struct sockaddr_in saddr;
	int saddrlen = sizeof(saddr);
	ret = native_fn_020a8c68(sock,(struct sockaddr *)&saddr, &saddrlen);
	if (gsiSocketIsError(ret))
		return 0;
	return saddr.sin_port;
}
