#include "context.h"
void native_main_020b6c90(int cookie)
{
	NATNegotiator neg = native_fn_020b6564(cookie);
	if (neg == NULL)
		return;
	if (neg->negotiateSock != INVALID_SOCKET)
		native_fn_020a8b6c(neg->negotiateSock);
	neg->negotiateSock = INVALID_SOCKET;
	neg->state = ns_canceled;
}
