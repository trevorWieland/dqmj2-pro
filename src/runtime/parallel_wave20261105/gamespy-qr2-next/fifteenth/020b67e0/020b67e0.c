#include "context.h"
void native_main_020b67e0(NATNegotiator neg, NegotiateResult result, SOCKET socket, struct sockaddr_in *remoteaddr)
{
	neg->result = result;
	neg->connectedSocket = socket;
	if(remoteaddr != NULL)
		copy8(&neg->remoteaddr, remoteaddr, sizeof(neg->remoteaddr));
	if(result == nr_inittimeout || result == nr_deadbeatpartner)
	{
		neg->state = ns_finished;
		neg->completedCallback(neg->result, neg->connectedSocket, (struct sockaddr_in *)&neg->remoteaddr, neg->userdata);
		native_fn_020b6c90(neg->cookie);
	}
	else
	{
		native_fn_020b6708(neg);
		neg->state = ns_reportsent;
		neg->retryTime = native_fn_020a8ef8() + REPORT_RETRY_TIME;
		neg->retryCount = 0;
		neg->maxRetryCount = REPORT_RETRY_COUNT;
	}
}
