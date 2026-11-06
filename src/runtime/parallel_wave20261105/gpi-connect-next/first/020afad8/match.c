#include "context.h"
void
native_main_020afad8(
  GPConnection * connection,
  GPIOperation * operation
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIOperation * pcurr = iconnection->operationList;
	GPIOperation * pprev = NULL;

	
	
	while(pcurr != NULL)
	{
		
		
		if(pcurr == operation)
		{
			
			
			if(pprev == NULL)
				iconnection->operationList = pcurr->pnext;
			else
				pprev->pnext = operation->pnext;

			gpiDestroyOperation(connection, operation);

			return;
		}

		pprev = pcurr;
		pcurr = pcurr->pnext;
	}
}
