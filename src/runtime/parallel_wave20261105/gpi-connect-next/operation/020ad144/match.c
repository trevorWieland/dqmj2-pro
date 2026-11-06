#include "context.h"
GPResult
native_main_020ad144(
  GPConnection * connection,
  const char nick[GP_NICK_LEN],
  const char uniquenick[GP_UNIQUENICK_LEN],
  const char email[GP_EMAIL_LEN],
  const char password[GP_PASSWORD_LEN],
  const char authtoken[GP_AUTHTOKEN_LEN],
  const char partnerchallenge[GP_PARTNERCHALLENGE_LEN],
  const char cdkey[GP_CDKEY_LEN],
  GPEnum firewall,
  GPIBool newuser,
  GPEnum blocking,
  GPCallback callback,
  void * param
)
{
	GPIConnectData * data;
	GPIOperation * operation;
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPResult result;

	
	
	if(iconnection->connectState == GPI_DISCONNECTED)
		CHECK_RESULT(gpiReset(connection));

	
	
	if(iconnection->connectState != GPI_NOT_CONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e09e8);

	
	
#if defined(GS_WIRELESS_DEVICE)
	GSI_UNUSED(firewall);
	iconnection->firewall = GPITrue;
#else
	switch(firewall)
	{
	case GP_FIREWALL:
		iconnection->firewall = GPITrue;
		break;
	case GP_NO_FIREWALL:
		iconnection->firewall = GPIFalse;
		break;
	default:
		Error(connection, GP_PARAMETER_ERROR, "Invalid firewall.");
	}
#endif

	
	
	strzcpy(iconnection->nick, nick, GP_NICK_LEN);
	strzcpy(iconnection->uniquenick, uniquenick, GP_UNIQUENICK_LEN);
	strzcpy(iconnection->email, email, GP_EMAIL_LEN);
	strzcpy(iconnection->password, password, GP_PASSWORD_LEN);

#ifdef GSI_UNICODE
	
	UTF8ToUCS2StringLen(iconnection->nick, iconnection->nick_W, GP_NICK_LEN);
	UTF8ToUCS2StringLen(iconnection->uniquenick, iconnection->uniquenick_W, GP_UNIQUENICK_LEN);
	UTF8ToUCS2StringLen(iconnection->email, iconnection->email_W, GP_EMAIL_LEN);
	UTF8ToUCS2StringLen(iconnection->password, iconnection->password_W, GP_PASSWORD_LEN);
#endif

	
	
	_strlwr(iconnection->email);

#ifdef GSI_UNICODE
	
	AsciiToUCS2String(iconnection->email, iconnection->email_W);
#endif

	
	
	data = (GPIConnectData *)gsimalloc(sizeof(GPIConnectData));
	if(data == NULL)
		Error(connection, GP_MEMORY_ERROR, native_data_020e09fc);
	memset(data, 0, sizeof(GPIConnectData));

	
	
	data->newuser = newuser;

	
	
	if(authtoken[0] && partnerchallenge[0])
	{
		strzcpy(data->authtoken, authtoken, GP_AUTHTOKEN_LEN);
		strzcpy(data->partnerchallenge, partnerchallenge, GP_PARTNERCHALLENGE_LEN);
	}

	
	
	if(cdkey)
		strzcpy(data->cdkey, cdkey, GP_CDKEY_LEN);

	
	
	CHECK_RESULT(gpiAddOperation(connection, GPI_CONNECT, data, &operation, blocking, callback, param));

	
	
	result = gpiStartConnect(connection, operation);
	if(result != GP_NO_ERROR)
	{
		operation->result = result;
		gpiFailedOpCallback(connection, operation);
		gpiDisconnect(connection, GPIFalse);
		return result;
	}

	
	
	if(operation->blocking)
		CHECK_RESULT(gpiProcess(connection, operation->id));

	return GP_NO_ERROR;
}
