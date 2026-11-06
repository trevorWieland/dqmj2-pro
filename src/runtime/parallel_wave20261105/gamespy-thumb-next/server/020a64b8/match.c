#include "context.h"
int native_main_020a64b8(const void *entry1, const void *entry2)
{
	GS_ASSERT(entry1)
	GS_ASSERT(entry2)
	if	(
			(((SBKeyValuePair *)entry1)->key == NULL)  ||
			(((SBKeyValuePair *)entry2)->key == NULL)  
		)
		return 1;

	return native_fn_02023f6c(((SBKeyValuePair *)entry1)->key, ((SBKeyValuePair *)entry2)->key);
}
