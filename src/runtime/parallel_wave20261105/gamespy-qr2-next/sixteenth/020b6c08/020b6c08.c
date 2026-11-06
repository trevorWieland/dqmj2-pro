#include "context.h"
NegotiateError native_main_020b6c08(SOCKET gamesocket, int cookie, int clientindex, NegotiateProgressFunc progresscallback, NegotiateCompletedFunc completedcallback, void *userdata)
{
	NATNegotiator neg;
	if(native_data_021d23ec != GSIACAvailable)
		return ne_socketerror;
	if (!native_fn_020b6b9c())
		return ne_dnserror;
	neg = native_fn_020b65a4();
	if (neg == NULL)
		return ne_allocerror;
	neg->gameSock = gamesocket;
	neg->clientindex = clientindex;
	neg->cookie = cookie;
	neg->progressCallback = progresscallback;
	neg->completedCallback = completedcallback;
	neg->userdata = userdata;
	neg->negotiateSock = native_fn_020a8b5c(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	neg->retryCount = 0;
	neg->gotRemoteData = 0;
	neg->sendGotRemoteData = 0;
	neg->guessedIP = 0;
	neg->guessedPort = 0;
	neg->maxRetryCount = 0;
	neg->result = nr_noresult;
	if (neg->negotiateSock == INVALID_SOCKET)
	{
		native_fn_020b65f8(neg);
		return ne_socketerror;
	}
	native_fn_020b6840(neg);
#if defined(GSI_COMMON_DEBUG)
	{
		struct sockaddr_in saddr;
		int namelen = sizeof(saddr);
		getsockname(neg->negotiateSock, (struct sockaddr *)&saddr, &namelen);
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
			"Negotiate Socket: %d\n", ntohs(saddr.sin_port));
	}
#endif
	return ne_noerror;
}
