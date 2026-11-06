#include "context.h"
GPResult
native_main_020ace1c(
  GPConnection * connection,
  int blockingOperationID
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPICallbackData * list;
	GPICallbackData * last;
	GPICallbackData * pcurr;
	GPICallbackData * pnext;
	GPICallbackData * pprev;

	if(blockingOperationID != 0)
	{
		list = iconnection->callbackList;
		last = iconnection->lastCallback;
		iconnection->callbackList = NULL;
		iconnection->lastCallback = NULL;

		pprev = NULL;
		for(pcurr = list ; pcurr != NULL ; )
		{
			pnext = pcurr->pnext;

			if((pcurr->operationID == blockingOperationID) || (pcurr->type == GPI_ADD_ERROR))
			{
				
				
				if(pprev != NULL)
					pprev->pnext = pcurr->pnext;
				else
					list = pcurr->pnext;
				if(last == pcurr)
					last = pprev;
	
				
				
				gpiCallCallback(connection, pcurr);
			}
			else
			{
				pprev = pcurr;
			}

			pcurr = pnext;
		}

		
		
		if(iconnection->callbackList != NULL)
		{
			iconnection->lastCallback->pnext = list;
			iconnection->lastCallback = last;
		}
		else
		{
			
			
			iconnection->callbackList = list;
			iconnection->lastCallback = last;
		}

		return GP_NO_ERROR;
	}

	while(iconnection->callbackList != NULL)
	{
		list = iconnection->callbackList;
		iconnection->callbackList = NULL;
		iconnection->lastCallback = NULL;

		for(pcurr = list ; pcurr != NULL ; pcurr = pnext)
		{
			pnext = pcurr->pnext;
			
			
			
			gpiCallCallback(connection, pcurr);
		}
	}

	return GP_NO_ERROR;
}
