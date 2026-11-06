#include "context.h"
SBState native_main_020a6978(ServerBrowser sb)
{
	if (sb->engine.querylist.count > 0)
		return sb_querying;
	if (sb->list.state == sl_mainlist || sb->list.state == sl_lanbrowse)
		return sb_listxfer;
	if (sb->list.state == sl_disconnected)
		return sb_disconnected;
	return sb_connected;
}