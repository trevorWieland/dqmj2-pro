#include "context.h"
char *native_main_020b3874(statsgame_t game,char *name, BucketFunc func,  char *value, int index)
{
	char fullname[64];
	sprintf(fullname, native_data_020e16d8,name, GetTeamIndex(game, index));
	return ServerOpString(game, fullname, func, value, index);
}
