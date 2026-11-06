#include "context.h"
gsi_bool native_main_020b753c(qr2_keybuffer_t keybuffer, int keyid)
{
	if (keybuffer->numkeys >= MAX_REGISTERED_KEYS)
		return gsi_false;
	if (keyid < 1 || keyid > MAX_REGISTERED_KEYS)
		return gsi_false;
	keybuffer->keys[keybuffer->numkeys++] = (uchar)keyid;
	return gsi_true;
}
