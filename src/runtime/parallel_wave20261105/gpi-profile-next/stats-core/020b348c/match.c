#include "context.h"
extern const char native_data_020e16a0[];
extern const char native_data_020e1688[];
extern const char native_data_020e166c[];
extern const char native_data_020e168c[];
void native_main_020b348c(const char *buf, int len)
{
	
	int reqindex;
	int pid;
	int lid;
	int success;
	int modified;
	success = atoi(value_for_key_safe(buf,native_data_020e16a0));
	pid = atoi(value_for_key_safe(buf,native_data_020e1688));
	lid = atoi(value_for_key_safe(buf,native_data_020e166c));
	modified = atoi(value_for_key_safe(buf,native_data_020e168c));
	reqindex = FindRequest(rt_savecb,lid,pid);
	if (reqindex == -1)
		return;
	CallReqCallback(reqindex,success,modified,NULL,0);
	
	GSI_UNUSED(len);
}
