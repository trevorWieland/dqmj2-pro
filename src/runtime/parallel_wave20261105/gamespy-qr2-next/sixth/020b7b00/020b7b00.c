#include "context.h"
gsi_bool native_main_020b7b00(qr2_t qrec, qr2_buffer_t buf, struct QRSplitQueryProgress* progress)
{
	unsigned char* packetNumPos = NULL;
	if (progress->mCurKeyType >= key_type_count)
		return gsi_false;
	if (AVAILABLE_BUFFER_LEN(buf) < 32)
		return gsi_false;
	native_fn_020b7588(buf, native_data_020e25b8);
	packetNumPos = (unsigned char*)&buf->buffer[buf->len++];
	*packetNumPos = (gsi_u8)progress->mCurPacketNum++;
	while (progress->mCurKeyType < key_type_count)
	{
		if (progress->mKeyBuffer.numkeys == 0)
			qrec->key_list_callback(progress->mCurKeyType, &progress->mKeyBuffer, qrec->udata);
		if (progress->mCurSubCount == 0 && progress->mCurKeyType != key_server)
			progress->mCurSubCount = qrec->playerteam_count_callback(progress->mCurKeyType, qrec->udata);
		if (AVAILABLE_BUFFER_LEN(buf) < 100)
			return gsi_true;
		buf->buffer[buf->len++] = (char)progress->mCurKeyType;
		while(progress->mCurKeyIndex < progress->mKeyBuffer.numkeys)
		{
			int aRegisteredKeyIndex = progress->mKeyBuffer.keys[progress->mCurKeyIndex];
			const char* aKeyName = native_data_020e277c[aRegisteredKeyIndex];
			if (gsi_is_false( native_fn_020b7588(buf,aKeyName) ))
				return gsi_true;
			if (progress->mCurKeyType == key_server)
			{
				qrec->server_key_callback(aRegisteredKeyIndex, buf, qrec->udata);
				if (AVAILABLE_BUFFER_LEN(buf) < 1)
					return gsi_true;
			}
			else
			{
				if (AVAILABLE_BUFFER_LEN(buf) < 1)
					return gsi_true;
				buf->buffer[buf->len++] = (char)progress->mCurSubIndex;
				while(progress->mCurSubIndex < progress->mCurSubCount)
				{
					if (progress->mCurKeyType == key_player)
						qrec->player_key_callback(aRegisteredKeyIndex, progress->mCurSubIndex, buf, qrec->udata);
					else if (progress->mCurKeyType == key_team)
						qrec->team_key_callback(aRegisteredKeyIndex, progress->mCurSubIndex, buf, qrec->udata);
					if (AVAILABLE_BUFFER_LEN(buf) < 1)
						return gsi_true;
					progress->mCurSubIndex++;
				}
				if (AVAILABLE_BUFFER_LEN(buf) > 0)
					buf->buffer[buf->len++] = '\0';
			}
			progress->mCurKeyIndex++;
			progress->mCurSubIndex = 0;
		}
		if (AVAILABLE_BUFFER_LEN(buf) > 0)
			buf->buffer[buf->len++] = '\0';
		progress->mCurKeyType = (qr2_key_type)(progress->mCurKeyType + 1);
		progress->mCurKeyIndex = 0;
		progress->mCurSubCount = 0;
		progress->mCurSubIndex = 0;
		progress->mKeyBuffer.numkeys = 0;
	}
	*packetNumPos |= QR2_SPLITNUM_FINALFLAG;
	return gsi_true;
}
