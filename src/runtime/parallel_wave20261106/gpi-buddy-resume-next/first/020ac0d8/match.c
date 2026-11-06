#include "context.h"
GPResult native_main_020ac0d8(GPConnection *connection, GPIPeer *peer)
{
	char *message;
	
	
	
	CHECK_RESULT(gpiSaveKeysToBuffer(connection, &message));
	
	
	if (message == NULL)
		message = (char*)native_data_020e0764;
	
	CHECK_RESULT(gpiSendBuddyMessage(connection, peer->profile, GPI_BM_KEYS_REPLY, message, GP_DONT_ROUTE, NULL));
	
	if (strcmp(message, native_data_020e0764)!= 0)
		freeclear(message);
	return GP_NO_ERROR;
}
