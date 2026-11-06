#include "context.h"
void native_main_020b7848(qr2_t qrec, qr2_buffer_t buf, char *challenge, int challengelen)
{
	char encrypted_val[MAX_CHALLENGE + 1];
	if(challengelen < 1)
		return;
	if (challengelen > (MAX_CHALLENGE + 1))
		return;
	if (challenge[challengelen - 1] != 0)
		return;
	native_fn_0201d6b8(encrypted_val, challenge);
	native_fn_020b7740((uchar *)qrec->secret_key, (int)native_fn_0201d69c(qrec->secret_key), (uchar *)encrypted_val, challengelen - 1);
	native_fn_020b76bc((uchar *)encrypted_val,challengelen - 1, (uchar *)(buf->buffer + buf->len));
	buf->len += (int)native_fn_0201d69c(buf->buffer + buf->len) + 1;
}
