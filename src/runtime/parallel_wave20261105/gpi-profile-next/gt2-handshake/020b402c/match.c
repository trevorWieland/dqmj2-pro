#include "context.h"
GT2Result native_main_020b402c
(
	GT2Connection connection,
	const GT2Byte * message,
	int len,
	GT2ConnectionCallbacks * callbacks
)
{
	char challenge[GTI2_CHALLENGE_LEN];

	
	gti2MessageCheck(&message, &len);

	
	if(len > 0)
	{
		connection->initialMessage = (char *)gsimalloc((unsigned int)len);
		if(!connection->initialMessage)
			return GT2OutOfMemory;

		memcpy(connection->initialMessage, message, (unsigned int)len);
		connection->initialMessageLen = len;
	}

	
	if(callbacks)
		connection->callbacks = *callbacks;

	
	gti2GetChallenge((GT2Byte *)challenge);

	
	gti2GetResponse((GT2Byte *)connection->response, (GT2Byte *)challenge);

	
	gti2SendClientChallenge(connection, challenge);

	
	connection->state = GTI2AwaitingServerChallenge;

	return GT2Success;
}
