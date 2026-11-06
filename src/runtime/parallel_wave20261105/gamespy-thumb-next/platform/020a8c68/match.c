#include "context.h"
int native_main_020a8c68(SOCKET sock, SOCKADDR* addr, int* len)
{
	int rcode;
	addr->len = (u8)*len;
	rcode = native_fn_020904ec(sock, addr);
	*len = addr->len;
	return native_fn_020a8b4c(rcode, NITRO_SOCKET_ERROR);
}