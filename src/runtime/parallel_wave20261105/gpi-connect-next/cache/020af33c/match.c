#include "context.h"
GPIBool
native_main_020af33c(
  GPConnection * connection,
  pGPIProfile  profile,
  const GPIInfoCache * cache
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;

	
	
	if(!iconnection->infoCaching)
		return GPITrue;

	
	
	gpiFreeInfoCache(profile);

	
	
	profile->cache = (GPIInfoCache *)gsimalloc(sizeof(GPIInfoCache));

	
	
	if(profile->cache)
	{
		*profile->cache = *cache;
		profile->cache->nick = goastrdup(cache->nick);
		profile->cache->uniquenick = goastrdup(cache->uniquenick);
		profile->cache->email = goastrdup(cache->email);
		profile->cache->firstname = goastrdup(cache->firstname);
		profile->cache->lastname = goastrdup(cache->lastname);
		profile->cache->homepage = goastrdup(cache->homepage);
		profile->cache->aimname = goastrdup(cache->aimname);
	}

	return (profile->cache != NULL) ? GPITrue:GPIFalse;
}