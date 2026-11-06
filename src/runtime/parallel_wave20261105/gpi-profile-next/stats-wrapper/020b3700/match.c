#include "context.h"
int native_main_020b3700(statsgame_t game, int tnum)
{
	FIXGAME(game, tnum);
	return *(int *)ArrayNth(game->teamnums,tnum);
}
