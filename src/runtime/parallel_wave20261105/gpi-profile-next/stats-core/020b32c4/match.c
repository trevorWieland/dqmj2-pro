#include "context.h"
int native_main_020b32c4(reqtype_t reqtype, int localid, int profileid)
{
	int i;
	serverreq_t *req;

	if (serverreqs == NULL)
		return -1;
	for (i = 0 ; i < ArrayLength(serverreqs); i++)
	{
		req = (serverreq_t *)ArrayNth(serverreqs, i);
		if (req->reqtype == reqtype && req->localid == localid && req->profileid == profileid)
			return i;
	}
	return -1;
	
}
