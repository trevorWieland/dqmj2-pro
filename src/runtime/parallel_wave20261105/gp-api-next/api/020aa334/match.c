#include "context.h"
#define freeclear(p) do{gsifree(p);(p)=NULL;}while(0)
GPResult native_main_020aa334(
  GPConnection * connection,
  GPProfile profile
)
{
	GPIConnection * iconnection;
	GPIProfile * pProfile;

	
	
	if((connection == NULL) || (*connection == NULL))
		return GP_PARAMETER_ERROR;

	
	
	iconnection = (GPIConnection*)*connection;
	if(iconnection->simulation)
		return GP_NO_ERROR;

	
	
	if(iconnection->connectState == GPI_DISCONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0440);

	
	
	if(!gpiGetProfile(connection, profile, &pProfile))
		return GP_NO_ERROR;

	
	
	pProfile->requestCount--;
	if(!iconnection->infoCaching && (pProfile->requestCount <= 0))
	{
		freeclear(pProfile->authSig);
		if(gpiCanFreeProfile(pProfile))
			gpiRemoveProfile(connection, pProfile);
	}

	return GP_NO_ERROR;
}
