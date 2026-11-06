#include "context.h"
GPIProfile *
native_main_020b0c2c(
  GPConnection * connection,
  int buddyIndex
)
{
	GPIFindProfileData data;
	data.index = buddyIndex;
	data.profile = NULL;
	gpiProfileMap(connection, gpiCheckForBuddy, &data);
	return data.profile;
}
