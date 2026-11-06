#include "context.h"
void
native_main_020acc9c(
  GPConnection * connection,
  GPICallbackData * data
)
{
	
	
	assert(data->callback.callback != NULL);
	assert(data->arg != NULL);
	data->callback.callback(connection, data->arg, data->callback.param);
	if(data->type == GPI_ADD_MESSAGE)
	{
		freeclear(((GPRecvBuddyMessageArg *)data->arg)->message);
	}
	else if (data->type == GPI_ADD_BUDDYUTM)
	{
		freeclear(((GPRecvBuddyUTMArg *)data->arg)->message);
	}
	else if(data->type == GPI_ADD_NICKS)
	{
		int i;
		GPGetUserNicksResponseArg * arg = (GPGetUserNicksResponseArg *)data->arg;

		for(i = 0 ; i < arg->numNicks ; i++)
		{
			freeclear(arg->nicks[i]);
			freeclear(arg->uniquenicks[i]);
		}
		freeclear(arg->nicks);
		freeclear(arg->uniquenicks);
	}
	else if(data->type == GPI_ADD_PMATCH)
	{
		GPFindPlayersResponseArg * arg = (GPFindPlayersResponseArg *)data->arg;

		freeclear(arg->matches);
	}
	else if(data->type == GPI_ADD_TRANSFER_CALLBACK)
	{
		GPTransferCallbackArg * arg = (GPTransferCallbackArg *)data->arg;

		if(arg->message)
			freeclear(arg->message);
	}
	else if(data->type == GPI_ADD_REVERSE_BUDDIES)
	{
		GPGetReverseBuddiesResponseArg * arg = (GPGetReverseBuddiesResponseArg *)data->arg;

		if(arg->profiles)
			freeclear(arg->profiles);
	}
	else if(data->type == GPI_ADD_SUGGESTED_UNIQUE)
	{
		int i;
		GPSuggestUniqueNickResponseArg * arg = (GPSuggestUniqueNickResponseArg *)data->arg;

		for(i = 0 ; i < arg->numSuggestedNicks ; i++)
		{
			freeclear(arg->suggestedNicks[i]);
		}
		freeclear(arg->suggestedNicks);
	}
	else if (data->type == GPI_ADD_BUDDYREVOKE)
	{
		GPRecvBuddyRevokeArg * arg = (GPRecvBuddyRevokeArg *)data->arg;

		
		gpiDeleteBuddy(connection, arg->profile, GPIFalse);
	}
	else if (data->type == GPI_ADD_REVERSE_BUDDIES_LIST)
	{
		GPGetReverseBuddiesListResponseArg * arg = (GPGetReverseBuddiesListResponseArg *)data->arg;

		if(arg->matches)
			freeclear(arg->matches);
	}
	else if (data->type == GPI_ADD_BUDDYKEYS)
	{
		GPGetBuddyStatusInfoKeysArg *arg = (GPGetBuddyStatusInfoKeysArg *)data->arg;
		if (arg->numKeys != 0)
		{
			int i;
			for (i=0; i < arg->numKeys; i++)
			{
				freeclear(arg->keys[i]);
				freeclear(arg->values[i]);
			}
			freeclear(arg->keys);
			freeclear(arg->values);
		}
	}
	freeclear(data->arg);
	freeclear(data);
}
