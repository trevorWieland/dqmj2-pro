#include "context.h"
GPResult native_main_020aa3e0(
  GPConnection * connection,
  int index, 
  GPBuddyStatus * status
)
{
	GPIConnection * iconnection;
	int num;
	GPIProfile * profile;
	if((connection == NULL) || (*connection == NULL))
		return GP_PARAMETER_ERROR;
	iconnection = (GPIConnection *)*connection;
	if(iconnection->simulation)
	{
		memset(status, 0, sizeof(GPBuddyStatus));
		return GP_NO_ERROR;
	}
	if(status == NULL)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e04bc);
	num = iconnection->profileList.numBuddies;
	if((index < 0) || (index >= num))
		Error(connection, GP_PARAMETER_ERROR, native_data_020e04cc);
	profile = gpiFindBuddy(connection, index);
	if(!profile)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e04cc);
	if(profile->buddyStatusInfo && profile->buddyStatusInfo->statusState==0)
	{
		status->profile=(GPProfile)profile->profileId;
		status->status=profile->buddyStatusInfo->statusState;
		status->statusString[0]='\0';
		status->locationString[0]='\0';
		status->ip=profile->buddyStatusInfo->buddyIp;
		status->port=profile->buddyStatusInfo->buddyPort;
		status->quietModeFlags=profile->buddyStatusInfo->quietModeFlags;
	}
	else
	{
	assert(profile->buddyStatus);
	status->profile = (GPProfile)profile->profileId;
	status->status = profile->buddyStatus->status;
#ifndef GSI_UNICODE
	if(profile->buddyStatus->statusString)
		strzcpy(status->statusString, profile->buddyStatus->statusString, GP_STATUS_STRING_LEN);
	else
		status->statusString[0] = '\0';
	if(profile->buddyStatus->locationString)
		strzcpy(status->locationString, profile->buddyStatus->locationString, GP_LOCATION_STRING_LEN);
	else
		status->locationString[0] = '\0';
#else
	if(profile->buddyStatus->statusString)
		UTF8ToUCS2String(profile->buddyStatus->statusString, status->statusString);
	else
		status->statusString[0] = '\0';
	if(profile->buddyStatus->locationString)
		UTF8ToUCS2String(profile->buddyStatus->locationString, status->locationString);
	else
		status->locationString[0] = '\0';
#endif
	status->ip = profile->buddyStatus->ip;
	status->port = profile->buddyStatus->port;
	status->quietModeFlags = profile->buddyStatus->quietModeFlags;
	}

	return GP_NO_ERROR;
}
