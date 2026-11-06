#include "context.h"
GT2Bool native_main_020b47c8(GT2Connection connection, GT2Byte * message, int len)
{
	char response[GTI2_RESPONSE_LEN];
	char challenge[GTI2_CHALLENGE_LEN];
	if(connection->state != GTI2AwaitingClientChallenge)
	{
		if(!native_fn_020b4634(connection))
			return GT2False;
		return GT2True;
	}
	if(len < GTI2_CHALLENGE_LEN)
	{
		if(!native_fn_020b4634(connection))
			return GT2False;
		return GT2True;
	}
	native_fn_020b3a58((GT2Byte *)response, message);
	native_fn_020b39c4((GT2Byte *)challenge);
	native_fn_020b3a58((GT2Byte *)connection->response, (GT2Byte *)challenge);
	if(!native_fn_020b5514(connection, response, challenge))
		return GT2False;
	connection->state = GTI2AwaitingClientResponse;
	return GT2True;
}
