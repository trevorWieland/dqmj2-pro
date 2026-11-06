#include "context.h"
GPIProfile *
native_main_020b09e0(
  GPConnection * connection,
  int id
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIProfileList * profileList = &iconnection->profileList;
	GPIProfile profile;
	GPIProfile * pProfile;

	assert(id > 0);

	
	
	if(id <= 0)
		return NULL;

	
	
	if(gpiGetProfile(connection, (GPProfile)id, &pProfile))
		return pProfile;

	
	
	memset(&profile, 0, sizeof(GPIProfile));
	profile.profileId = id;
	profile.userId = 0;
	profile.cache = NULL;
	profile.authSig = NULL;
	profile.peerSig = NULL;
	profile.requestCount = 0;

	
	
	TableEnter(profileList->profileTable, &profile);

	
	
	profileList->num++;

	
	
	if(gpiGetProfile(connection, (GPProfile)id, &pProfile))
		return pProfile;

	
	
	return NULL;
}
