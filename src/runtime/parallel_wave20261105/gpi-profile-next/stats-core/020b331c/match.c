#include "context.h"
extern const char native_data_020e1664[];
extern const char native_data_020e166c[];
extern const char native_data_020e1670[];
void native_main_020b331c(const char *buf, int len)
{
	
	int reqindex;
	char *errmsg;
	int pid;
	int lid;
	pid = atoi(value_for_key_safe(buf,native_data_020e1664));
	lid = atoi(value_for_key_safe(buf,native_data_020e166c));
	errmsg = value_for_key_safe(buf,native_data_020e1670);
	reqindex = FindRequest(rt_authcb,lid,0);
	if (reqindex == -1)
		return;
	((serverreq_t *)ArrayNth(serverreqs, reqindex))->profileid = pid;
	CallReqCallback(reqindex,(pid > 0),0, errmsg,0);
	
	GSI_UNUSED(len);
}
