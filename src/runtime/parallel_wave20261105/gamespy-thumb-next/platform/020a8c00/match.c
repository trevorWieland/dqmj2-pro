#include "context.h"
int native_main_020a8c00(SOCKET sock, char* buf, int len, int flags, SOCKADDR* addr, int* fromlen)
{
	int rcode;
	addr->len = (u8)*fromlen;
	rcode = native_fn_02090378(sock, buf, len, flags, addr);
	*fromlen = addr->len;
	return native_fn_020a8b4c(rcode, NITRO_SOCKET_ERROR);
}