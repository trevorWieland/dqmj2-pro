#include "context.h"
void native_main_020af494(GPConnection * connection)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	if (iconnection->extendedInfoKeys)
	{
		ArrayFree(iconnection->extendedInfoKeys);
		iconnection->extendedInfoKeys = NULL;
	}
}
