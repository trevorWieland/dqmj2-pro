#include "context.h"
GT2Bool native_main_020b4a30(GT2Connection connection, GTI2MessageType type, GT2Byte * message, int len)
{
	connection->expectedSerialNumber++;
	if(type == GTI2MsgAppReliable)
	{
		if(!native_fn_020b475c(connection, message, len))
			return GT2False;
	}
	else if(type == GTI2MsgClientChallenge)
	{
		if(!native_fn_020b47c8(connection, message, len))
			return GT2False;
	}
	else if(type == GTI2MsgServerChallenge)
	{
		if(!native_fn_020b4834(connection, message, len))
			return GT2False;
	}
	else if(type == GTI2MsgClientResponse)
	{
		if(!native_fn_020b48c8(connection, message, len))
			return GT2False;
	}
	else if(type == GTI2MsgAccept)
	{
		if(!native_fn_020b4984(connection))
			return GT2False;
	}
	else if(type == GTI2MsgReject)
	{
		if(!native_fn_020b49b8(connection, message, len))
			return GT2False;
	}
	else if(type == GTI2MsgClose)
	{
		if(!native_fn_020b4a00(connection))
			return GT2False;
	}
	else if(type == GTI2MsgKeepAlive)
	{
	}
	return GT2True;
}
