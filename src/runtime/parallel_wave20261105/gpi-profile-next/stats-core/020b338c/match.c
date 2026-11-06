#include "context.h"
extern const char native_data_020e1678[];
extern const char native_data_020e166c[];
void native_main_020b338c(const char *buf, int len)
{
	
	int reqindex;
	int pid;
	int lid;
	pid = atoi(value_for_key_safe(buf,native_data_020e1678));
	lid = atoi(value_for_key_safe(buf,native_data_020e166c));
	reqindex = FindRequest(rt_profilecb,lid,0);
	if (reqindex == -1)
		return;
	((serverreq_t *)ArrayNth(serverreqs, reqindex))->profileid = pid;
	CallReqCallback(reqindex,(pid > 0),0,NULL,0);
	
	GSI_UNUSED(len);
}
