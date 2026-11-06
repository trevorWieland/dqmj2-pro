#include "context.h"
void native_main_020b75cc()
{
	struct hostent *phost;
	phost = native_fn_020a8dc0();
	if (phost == NULL)
		return;
	for (native_data_021d2ec8 = 0 ; native_data_021d2ec8 < MAX_LOCAL_IP ; native_data_021d2ec8++)
	{
		if (phost->h_addr_list[native_data_021d2ec8] == 0)
			break;
		copy4(&native_data_021d2ecc[native_data_021d2ec8], phost->h_addr_list[native_data_021d2ec8]);
	}
}
