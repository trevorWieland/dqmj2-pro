#include "context.h"
SBError native_main_020a834c(SBServerList *slist, goa_uint32 ip, unsigned short port, const char *data, int len)
{
	char requestBuffer[16];
	unsigned short tmp;
	unsigned short msgLen = 9;
	SBError ret;
	int i;
	
	if (slist->state == sl_disconnected) 
		native_fn_020a7404(slist, NULL, NULL, NO_SERVER_LIST, 0); 

	if (slist->state == sl_disconnected)
		return sbe_connecterror;

	
	tmp = htons((unsigned short)(msgLen + len));
	memcpy(requestBuffer, &tmp, 2);
	
	requestBuffer[2] = SEND_MESSAGE_REQUEST;
	memcpy(requestBuffer + 3, &ip, sizeof(ip));
	memcpy(requestBuffer + 7, &port, sizeof(port));	
	ret = native_fn_020a7390(slist, requestBuffer, msgLen);
	if (ret != sbe_noerror)
		return ret;
	i = native_fn_020a8c24(slist->slsocket, data, len, 0); 
	if (i < 0)
		return sbe_connecterror;
	return sbe_noerror;
	
}