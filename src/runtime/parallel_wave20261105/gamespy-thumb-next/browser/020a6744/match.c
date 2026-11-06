#include "context.h"
ServerBrowser native_main_020a6744(const char *queryForGamename, const char *queryFromGamename, const char *queryFromKey, int queryFromVersion, int maxConcUpdates, int queryVersion, SBBool lanBrowse, ServerBrowserCallback callback, void *instance)
{
	ServerBrowser sb;
	if(lanBrowse == SBFalse)
	{
		if(native_data_021d23ec != GSIACAvailable)
			return NULL;
	}
	
	sb = (ServerBrowser)native_fn_020a927c(sizeof(struct _ServerBrowser));
	if (sb == NULL)
		return NULL;
	sb->BrowserCallback = callback;
	
	sb->instance = instance;
	sb->dontUpdate = SBFalse;
	native_fn_020a6fc4(&sb->list, queryForGamename, queryFromGamename, queryFromKey, queryFromVersion, lanBrowse, native_fn_020a6564, sb);
	native_fn_020a5a74(&sb->engine, maxConcUpdates, queryVersion, lanBrowse, native_fn_020a66c0, sb);
	return sb;
}