#include "context.h"
extern const char native_data_020e16a8[];
extern const char native_data_020e16b4[];
extern const char native_data_020e16c0[];
extern const char native_data_020e16cc[];
void native_main_020b34f8(char *buff, int len)
{
	

	buff[len] = 0;
	
	if (strncmp(buff,native_data_020e16a8,8) == 0)
	{
		ProcessPlayerAuth(buff, len);
	} else if (strncmp(buff,native_data_020e16b4,9) == 0)
	{
		ProcessGetPid(buff, len);
	} else if (strncmp(buff,native_data_020e16b4,9) == 0)
	{
		ProcessGetPid(buff, len);
	} else if (strncmp(buff,native_data_020e16c0,8) == 0)
	{
		ProcessGetData(buff, len);
	} else if (strncmp(buff,native_data_020e16cc,8) == 0)
	{
		ProcessSetData(buff, len);
	}
	
}
