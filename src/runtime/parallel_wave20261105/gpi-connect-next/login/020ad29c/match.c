#include "context.h"
GPResult
native_main_020ad29c(
  GPConnection * connection,
  GPIConnectData * data
)
{
	char buffer[512];
	char response[33];
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIProfile * profile;
	char * passphrase;
	char userBuffer[GP_NICK_LEN + GP_EMAIL_LEN];
	char partnerBuffer[11];
	char * user;

	
	
	randomString(data->userChallenge, sizeof(data->userChallenge) - 1);

	
	
	if(data->partnerchallenge[0])
		passphrase = data->partnerchallenge;
	else
		passphrase = iconnection->password;
	MD5Digest((unsigned char*)passphrase, strlen(passphrase), data->passwordHash);

	
	
	if(iconnection->partnerID != GP_PARTNERID_GAMESPY)
	{
		sprintf(partnerBuffer, native_data_020e0a0c, iconnection->partnerID);
	}
	else
	{
		
		memcpy(partnerBuffer,native_data_020e0a10,1);
	}

	if(data->authtoken[0])
		user = data->authtoken;
	else if(iconnection->uniquenick[0])
	{
		sprintf(userBuffer, native_data_020e0a14, partnerBuffer, iconnection->uniquenick);
		user = userBuffer;
	}
	else
	{
		sprintf(userBuffer, native_data_020e0a1c, partnerBuffer, iconnection->nick, iconnection->email);
		user = userBuffer;
	}

	
	
	sprintf(buffer, native_data_020e0a24,
		data->passwordHash,
		native_data_020e0a34,
		user,
		data->userChallenge,
		data->serverChallenge,
		data->passwordHash);
	MD5Digest((unsigned char *)buffer, strlen(buffer), response);

	
	
	if(iconnection->infoCaching)
	{
		gpiFindProfileByUser(connection, iconnection->nick, iconnection->email, &profile);
		if(profile != NULL)
		{
			
			
			iconnection->userid = profile->userId;
			iconnection->profileid = profile->profileId;
		}
	}

	
	
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0a68);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0a70);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, data->userChallenge);
	if(data->authtoken[0])
	{
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0a7c);
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, data->authtoken);
	}
	else if(iconnection->uniquenick[0])
	{
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0a88);
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, iconnection->uniquenick);
	}
	else
	{
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0a98);
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, iconnection->nick);
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0aa0);
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, iconnection->email);
	}
	if(iconnection->userid != 0)
	{
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0aa4);
		gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->userid);
	}
	if(iconnection->profileid != 0)
	{
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0ab0);
		gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->profileid);
	}
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0abc);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->partnerID);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0ac8);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, response);
	if(iconnection->firewall == GP_FIREWALL)
		gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0ad4);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0ae0);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->peerPort);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0ae8);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->productID);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0af4);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, __GSIACGamename);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b00);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->namespaceID);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b10);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, GPI_SDKREV);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b20);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->quietModeFlags);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b28);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0b30);

	return GP_NO_ERROR;
}
