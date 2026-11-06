#include "context.h"
GPIBool
native_main_020b0a50(
  GPConnection * connection,
  GPProfile profileid,
  GPIProfile ** pProfile
)
{
	GPIProfile * profile;
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIProfile profileTemp;

	profileTemp.profileId = profileid;
	profile = (GPIProfile *)TableLookup(iconnection->profileList.profileTable, &profileTemp);
	if(pProfile)
		*pProfile = profile;

	return ((profile != NULL) ? GPITrue:GPIFalse);
}
