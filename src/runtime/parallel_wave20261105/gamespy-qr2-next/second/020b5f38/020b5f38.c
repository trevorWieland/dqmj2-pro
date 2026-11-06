#include "context.h"
const char * native_main_020b5f38(unsigned int ip, unsigned short port, char string[22])
{
	char * strAddress;
	if(string)
		strAddress = string;
	else
	{
		native_data_021d2948 ^= 1;
		strAddress = native_data_021d294c[native_data_021d2948];
	}
	if(ip)
	{
		IN_ADDR inAddr;
		inAddr.s_addr = ip;
		if(port)
			native_fn_0200616c(strAddress, native_data_020e1718, native_fn_0209073c(inAddr), port);
		else
			native_fn_0200616c(strAddress, native_data_020e1720, native_fn_0209073c(inAddr));
	}
	else if(port)
		native_fn_0200616c(strAddress, native_data_020e1724, port);
	else
		strAddress[0] = '\0';
	return strAddress;
}
