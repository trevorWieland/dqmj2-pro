#include "context.h"
GPResult native_main_020ac130(GPConnection *connection, GPIPeer *peer, char *buffer)
{
	GPIProfile *pProfile;
		
	
	
	
	if(!gpiGetProfile(connection, peer->profile, &pProfile))
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0768);
	
	
	if (strcmp(buffer, native_data_020e0764) == 0)
	{
		GPIPeerOp *anIterator;
		
		for (anIterator = peer->peerOpQueue.first; anIterator != NULL; anIterator = anIterator->next)
			if (anIterator->type == GPI_BM_KEYS_REQUEST)
				break;
		
		if (!anIterator)
		{
			return GP_NO_ERROR;
		}
		else if (anIterator->type == GPI_BM_KEYS_REQUEST && anIterator->callback)
		{
			GPGetBuddyStatusInfoKeysArg *arg = (GPGetBuddyStatusInfoKeysArg *)gsimalloc(sizeof(GPGetBuddyStatusInfoKeysArg));
			GPICallback callback;
			callback.callback = anIterator->callback;
			callback.param = anIterator->userData;
			
			arg->keys = NULL;
			arg->numKeys = 0;
			arg->values = NULL;
			arg->profile = peer->profile;
			gpiAddCallback(connection, callback, arg, NULL, 0);
			gpiPeerRemoveOp(peer, anIterator);
		}
	}
	else
	{
		int decodedLen = 0,
			index = 0, numKeys, i;
		char keyName[512];
		char keyVal[512];
		char decodeKey[512];
		char decodeVal[512];
		gsi_char **keys;
		gsi_char **values;
		GPIPeerOp *anIterator;
		char *checkKey = NULL;

		
		gpiReadKeyAndValue(connection, buffer, &index,  keyName, keyVal);
		
		
		if (strcmp(keyName, native_data_020e077c) != 0)
			CallbackError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e0784);
		
		numKeys = atoi(keyVal);

		if (numKeys == 0)
		{
			GPIPeerOp *anIterator;
			
			for (anIterator = peer->peerOpQueue.first; anIterator != NULL; anIterator = anIterator->next)
				if (anIterator->type == GPI_BM_KEYS_REQUEST)
					break;

			if (!anIterator)
			{
				return GP_NO_ERROR;
			}
			else if (anIterator->type == GPI_BM_KEYS_REQUEST && anIterator->callback)
			{
				GPGetBuddyStatusInfoKeysArg *arg = (GPGetBuddyStatusInfoKeysArg *)gsimalloc(sizeof(GPGetBuddyStatusInfoKeysArg));
				GPICallback callback;
				callback.callback = anIterator->callback;
				callback.param = anIterator->userData;

				arg->keys = NULL;
				arg->numKeys = 0;
				arg->values = NULL;
				arg->profile = peer->profile;
				gpiAddCallback(connection, callback, arg, NULL, 0);
				gpiPeerRemoveOp(peer, anIterator);
			}
		}
		else
		{
			keys = (gsi_char **)gsimalloc(sizeof(gsi_char *) * numKeys);
			values = (gsi_char **)gsimalloc(sizeof(gsi_char *) * numKeys);

			for (i = 0; i < numKeys; i++)
			{			
				gpiReadKeyAndValue(connection, buffer, &index,  keyName, keyVal);
				B64Decode(keyName, decodeKey, (int)strlen(keyName), &decodedLen, 2);
				decodeKey[decodedLen] = '\0';
				B64Decode(keyVal, decodeVal, (int)strlen(keyVal), &decodedLen, 2);
				decodeVal[decodedLen] = '\0';
	
				keys[i] = goastrdup(decodeKey);
				values[i] = goastrdup(decodeVal);
	

				if (gpiStatusInfoCheckKey(connection, pProfile->buddyStatusInfo->extendedInfoKeys, decodeKey, &checkKey) == GP_NO_ERROR
					&& checkKey == NULL)
				{
					gpiStatusInfoAddKey(connection, pProfile->buddyStatusInfo->extendedInfoKeys, decodeKey, decodeVal);
				}
				else
				{
					gpiStatusInfoSetKey(connection, pProfile->buddyStatusInfo->extendedInfoKeys, decodeKey, decodeVal);
				}
			}
			
			for (anIterator = peer->peerOpQueue.first; anIterator != NULL; anIterator = anIterator->next)
				if (anIterator->type == GPI_BM_KEYS_REQUEST)
					break;

			if (!anIterator)
			{
				return GP_NO_ERROR;
			}
			else if (anIterator->type == GPI_BM_KEYS_REQUEST && anIterator->callback)
			{
				GPICallback callback;
				GPGetBuddyStatusInfoKeysArg *arg = (GPGetBuddyStatusInfoKeysArg *)gsimalloc(sizeof(GPGetBuddyStatusInfoKeysArg));
				
				callback.callback = anIterator->callback;
				callback.param = anIterator->userData;
				
				
				arg->numKeys = numKeys;

				arg->keys = keys;
				arg->values = values;
				arg->profile = peer->profile;
				
				gpiAddCallback(connection, callback, arg, NULL, GPI_ADD_BUDDYKEYS);
				gpiPeerRemoveOp(peer, anIterator);
			}
		}
	}
	
	return GP_NO_ERROR;
}
