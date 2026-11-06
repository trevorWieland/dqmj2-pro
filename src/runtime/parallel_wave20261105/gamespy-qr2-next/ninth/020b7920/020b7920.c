#include "context.h"
void native_main_020b7920(qr2_t qrec, qr2_buffer_t buf, qr2_key_type keytype, int keycount, uchar *keys)
{
	struct qr2_keybuffer_s kb;
	int playerteamcount;
	unsigned short cttemp;
	int i;
	int pindex;
	const char *k;
	int len;
	kb.numkeys = 0;
	if (keycount == 0)
		return;
	if (keytype == key_player || keytype == key_team)
	{
		if (AVAILABLE_BUFFER_LEN(buf) < sizeof(cttemp))
			return;
		playerteamcount = qrec->playerteam_count_callback(keytype, qrec->udata);
		cttemp = htons((unsigned short)playerteamcount);
		memcpy(buf->buffer + buf->len, &cttemp, sizeof(cttemp));
		buf->len += sizeof(cttemp);
	} else
		playerteamcount = 1;
	if (keycount == 0xFF)
	{
		qrec->key_list_callback(keytype, &kb, qrec->udata);
		for (i = 0 ; i < kb.numkeys ; i++)
		{
			k = native_data_020e277c[kb.keys[i]];
			if (k == NULL)
				k = native_data_020e25ac;
			native_fn_020b7588(buf, k);
			if (keytype == key_server)
			{
				len = buf->len;
				qrec->server_key_callback(kb.keys[i], buf, qrec->udata);
				if(len == buf->len)
					native_fn_020b7588(buf, native_data_020e25b4);
			}
		}
		if (AVAILABLE_BUFFER_LEN(buf) < 1)
			return;
		buf->buffer[buf->len++] = 0;
		keycount = kb.numkeys;
		keys = kb.keys;
		if (keytype == key_server)
			return;
	}
	for (pindex = 0 ; pindex < playerteamcount ; pindex++)
	{
		for (i = 0 ; i < keycount ; i++)
		{
			len = buf->len;
			if (keytype == key_server)
				qrec->server_key_callback(keys[i], buf, qrec->udata);
			else if (keytype == key_player)
				qrec->player_key_callback(keys[i], pindex, buf, qrec->udata);
			else if (keytype == key_team)
				qrec->team_key_callback(keys[i], pindex, buf, qrec->udata);
			if(len == buf->len)
				native_fn_020b7588(buf, native_data_020e25b4);
		}
	}
}
