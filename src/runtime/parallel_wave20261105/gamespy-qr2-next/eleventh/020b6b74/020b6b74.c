#include "context.h"
unsigned int native_main_020b6b74(const char * overrideHostname, const char * defaultHostname)
{
	const char * hostname;
	char hostnameBuffer[64];
	if(overrideHostname == NULL)
	{
		native_fn_020061ac(hostnameBuffer, sizeof(hostnameBuffer), native_data_020e1740, native_data_021d23f0, defaultHostname);
		hostname = hostnameBuffer;
	}
	else
	{
		hostname = overrideHostname;
	}
	return native_fn_020b6b4c(hostname);
}
