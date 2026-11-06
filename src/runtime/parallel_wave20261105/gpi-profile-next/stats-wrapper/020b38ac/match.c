#include "context.h"
int native_main_020b38ac(statsgame_t game,char *name, BucketFunc func,  int value, int index)
{
	char fullname[64];
	sprintf(fullname, native_data_020e16e0,name, GetPlayerIndex(game, index));
	return ServerOpInt(game, fullname, func, value, index);
}
