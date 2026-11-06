#include "context.h"
GPResult
native_main_020b27a0(
  GPConnection * connection
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIOperation ** searchList;
	GPIOperation * operation;
	GPISearchData * data;
	GPResult result;
	int num = 0;
	int i;

	
	
	if(iconnection->numSearches > 0)
	{
		
		
		searchList = (GPIOperation **)gsimalloc(sizeof(GPIOperation *) * iconnection->numSearches);
		if(searchList == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e1170);

		
		
		for(operation = &iconnection->operationList[0] ; operation != NULL ; operation = operation->pnext)
		{
			
			
			if((operation->type == GPI_PROFILE_SEARCH) && (operation->state != GPI_FINISHING))
			{
				
				
				if(!((GPISearchData *)operation->data)->processing)
				{
					assert(num < iconnection->numSearches);
					searchList[num++] = operation;
					((GPISearchData *)operation->data)->processing = GPITrue;
				}
			}
		}

		
		
		for(i = 0 ; i < num ; i++)
		{
			result = gpiProcessSearch(connection, searchList[i]);
			if(result != GP_NO_ERROR)
				searchList[i]->result = result;
		}

		
		
		for(i = 0 ; i < num ; i++)
		{
			data = ((GPISearchData *)searchList[i]->data);
			data->processing = GPIFalse;
			if(data->remove)
				gpiRemoveOperation(connection, searchList[i]);
		}

		freeclear(searchList);
	}

	return GP_NO_ERROR;
}
