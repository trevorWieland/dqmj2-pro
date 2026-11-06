#include "context.h"
GPResult
native_main_020ad63c(
  GPConnection * connection,
  GPIConnectData * data
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	size_t i;
	const int useAlternateEncoding = 1;

	
	char passwordenc[GP_PASSWORDENC_LEN];
	gpiEncodeString(iconnection->password, passwordenc);

	
	
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b38);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b44);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, iconnection->email);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b4c);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, iconnection->nick);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b54);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, passwordenc);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0ae8);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->productID);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0af4);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, __GSIACGamename);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b00);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->namespaceID);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0a88);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, iconnection->uniquenick);
	if(data->cdkey[0])
	{
		
		char cdkeyxor[GP_CDKEY_LEN];
		char cdkeyenc[GP_CDKEYENC_LEN];
		size_t cdkeylen = strlen(data->cdkey);
		
		Util_RandSeed((unsigned long)GP_XOR_SEED);
		for (i=0; i < cdkeylen; i++)
		{
			
			char aRand = (char)Util_RandInt(0, 0xFF);
			cdkeyxor[i] = (char)(data->cdkey[i] ^ aRand);
		}
		cdkeyxor[i] = '\0';

		
		B64Encode(cdkeyxor, cdkeyenc, (int)cdkeylen, useAlternateEncoding);

		
		
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b64);
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, cdkeyenc);
	}
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0abc);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->partnerID);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b28);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b30);

	return GP_NO_ERROR;
}
