#include "context.h"

void native_main_020b35dc(int reqindex, int success, time_t modified, char *data, int length)
{
	serverreq_t *req;
	if (reqindex < 0 || reqindex >= ArrayLength(serverreqs))
		return;
	req = (serverreq_t *)ArrayNth(serverreqs, reqindex);
	if (req->callback)
		switch (req->reqtype)
		{
		case rt_authcb:
((PersAuthCallbackFn )req->callback)(req->localid, req->profileid, success, data, req->instance);

			break;
		case rt_datacb:
			((PersDataCallbackFn )req->callback)(req->localid,req->profileid,req->pdtype, req->pdindex, success, modified, data, length, req->instance);
			break;
		case rt_savecb:
			((PersDataSaveCallbackFn )req->callback)(req->localid, req->profileid, req->pdtype, req->pdindex,success, modified, req->instance);
			break;
		case rt_profilecb:
			((ProfileCallbackFn )req->callback)(req->localid, req->profileid, success, req->instance);
			break;
		}
	ArrayDeleteAt(serverreqs,reqindex);
}
