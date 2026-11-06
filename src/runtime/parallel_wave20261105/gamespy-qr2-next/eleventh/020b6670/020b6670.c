#include "context.h"
void native_main_020b6670(SOCKET sock, unsigned int toaddr, unsigned short toport, void *data, int len)
{
	struct sockaddr_in saddr;
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons(toport);
	saddr.sin_addr.s_addr = toaddr;
	native_fn_020a8c34(sock, (char *)data, len, 0, (struct sockaddr *)&saddr, sizeof(saddr));
}
