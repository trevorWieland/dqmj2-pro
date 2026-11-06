#include "context.h"
GPResult
native_main_020b0b90(
  GPConnection * connection,
  char nick[GP_NICK_LEN],
  char email[GP_EMAIL_LEN],
  GPIProfile ** profile
)
{
	GPIFindProfileByUserData data;
	data.nick = nick;
	data.email = email;
	data.profile = profile;
	data.found = GPIFalse;
	gpiProfileMap(connection, gpiCheckProfileForUser, &data);
	if(!data.found)
		*profile = NULL;
	return GP_NO_ERROR;
}
