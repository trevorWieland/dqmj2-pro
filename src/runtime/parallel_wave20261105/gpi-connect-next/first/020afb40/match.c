#include "context.h"
GPIBool
native_main_020afb40(
  const GPConnection * connection
)
{
	GPIOperation * operation;
	GPIConnection * iconnection = (GPIConnection*)*connection;

	
	
	for(operation = iconnection->operationList ; operation != NULL ; operation = operation->pnext)
	{
		
		
		if((operation->blocking) && (operation->type != GPI_PROFILE_SEARCH))
			return GPITrue;
	}

	
	
	return GPIFalse;
}
