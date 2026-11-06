#include "context.h"
gsi_bool native_main_020b6aa8(SOCKET sock)
{
	gsi_bool active = gsi_true;
	gsi_bool success = gsi_false;
	if(sock != INVALID_SOCKET)
	{
		if(native_fn_020a8ef8() - natifyStartTime < NATIFY_TIMEOUT)
			active = native_fn_020b6334(sock, &nat);
		else
			active = gsi_false;
		if(!active)
		{
			success = native_fn_020b633c(&nat);
			natifyCallback(success, nat);
			native_data_020e172c.kind = native_data_021d2c70.kind;
			native_data_021d2bc4.scheme = native_data_021d2c70.scheme;
			if (mappingSock != INVALID_SOCKET)
				native_fn_020a8b6c(mappingSock);
			mappingSock = INVALID_SOCKET;
			if (ertSock != INVALID_SOCKET)
				native_fn_020a8b6c(ertSock);
			ertSock = INVALID_SOCKET;
		}
	}
	return(active);
}
