#include "context.h"
void native_main_020b5f14(GT2Socket socket)
{
	if(socket->error)
		return;
	socket->error = GT2True;
	native_fn_020b4540(socket);
	if(!native_fn_020b3be4(socket))
		return;
	native_fn_020b5b4c(socket);
}
