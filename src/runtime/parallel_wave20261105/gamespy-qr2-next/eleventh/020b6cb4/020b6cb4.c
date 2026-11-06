#include "context.h"
void native_main_020b6cb4(NATNegotiator neg)
{
	struct sockaddr_in saddr;
	int saddrlen = sizeof(struct sockaddr_in);
	int error;
	if(activeNatify)
	{
		activeNatify = native_fn_020b6aa8(mappingSock);
		activeNatify = native_fn_020b6aa8(ertSock);
	}
	if(neg == NULL)
		return;
	if (neg->state == ns_canceled)
	{
		gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Memory, GSIDebugLevel_Notice,
			"Removing canceled negotiator\n");
		native_fn_020b65f8(neg);
		return;
	}
	if (neg->negotiateSock != INVALID_SOCKET)
	{
		while (native_fn_020a8d88(neg->negotiateSock))
		{
			error = native_fn_020a8c00(neg->negotiateSock, native_data_021d2cc8, NNINBUF_LEN, 0, (struct sockaddr *)&saddr, &saddrlen);
			if (gsiSocketIsError(error))
			{
				gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
					"RECV SOCKET ERROR: %d\n", GOAGetLastError(neg->negotiateSock));
				break;
			}
			native_fn_020b70c8(native_data_021d2cc8, error, &saddr);
			if (neg->state == ns_canceled)
				break;
			if (neg->negotiateSock == INVALID_SOCKET)
				break;
		}
	}
	if (neg->state == ns_initsent || neg->state == ns_connectping)
	{
		if (native_fn_020a8ef8() > neg->retryTime)
		{
			if (neg->retryCount > neg->maxRetryCount)
			{
				gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
					"RETRY FAILED...\n");
				if(neg->state == ns_initsent)
					native_fn_020b67e0(neg, nr_inittimeout, INVALID_SOCKET, NULL);
				else
					native_fn_020b67e0(neg, nr_pingtimeout, INVALID_SOCKET, NULL);
			} else
			{
				neg->retryCount++;
				if (neg->state == ns_initsent)
					native_fn_020b6840(neg);
				else
					native_fn_020b69e4(neg);
				gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
					"[retry]\n");
			}
		}
	}
	if (neg->state == ns_finished && native_fn_020a8ef8() > neg->retryTime)
	{
		struct sockaddr_in saddr;
		saddr.sin_family = AF_INET;
		saddr.sin_port = htons(neg->guessedPort);
		saddr.sin_addr.s_addr = neg->guessedIP;
		if (neg->gameSock == INVALID_SOCKET)
			native_fn_020b67e0(neg, nr_success, neg->negotiateSock, (struct sockaddr_in *)&saddr);
		else
			native_fn_020b67e0(neg, nr_success, neg->gameSock, (struct sockaddr_in *)&saddr);
	}
	if (neg->state == ns_initack && native_fn_020a8ef8() > neg->retryTime)
	{
		native_fn_020b67e0(neg, nr_deadbeatpartner, INVALID_SOCKET, NULL);
	}
	if(neg->state == ns_reportsent && native_fn_020a8ef8() > neg->retryTime)
	{
		if(neg->retryCount > neg->maxRetryCount)
		{
			gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
				"REPORT retry FAILED...\n");
			neg->completedCallback(neg->result, neg->connectedSocket, (struct sockaddr_in *)&neg->remoteaddr, neg->userdata);
			if (neg->gameSock == INVALID_SOCKET)
				neg->negotiateSock = INVALID_SOCKET;
			native_fn_020b6c90(neg->cookie);
		}
		else
		{
			native_fn_020b6708(neg);
			neg->retryCount++;
			neg->retryTime = native_fn_020a8ef8() + REPORT_RETRY_TIME;
			gsDebugFormat(GSIDebugCat_NatNeg, GSIDebugType_Network, GSIDebugLevel_Notice,
				"[retry]\n");
		}
	}
}
