#include "context.h"
int native_main_020b760c(const char *host, int port, struct sockaddr_in *saddr, struct hostent **savehent)
{
	struct hostent *hent = NULL;
	saddr->sin_family = AF_INET;
	saddr->sin_port = htons((unsigned short)port);
	if (host == NULL)
		saddr->sin_addr.s_addr = INADDR_ANY;
	else
		saddr->sin_addr.s_addr = native_fn_020a8c84(host);
	if (saddr->sin_addr.s_addr == INADDR_NONE && native_fn_0201d800(host,native_data_020e2590) != 0)
	{
		hent = native_fn_0209046c(host);
		if (!hent)
			return 0;
		saddr->sin_addr.s_addr = *(unsigned int *)hent->h_addr_list[0];
	}
	if (savehent != NULL)
		*savehent = hent;
	return 1;
}
