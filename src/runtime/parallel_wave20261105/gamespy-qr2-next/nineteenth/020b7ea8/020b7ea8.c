#include "context.h"
int native_main_020b7ea8(qr2_t qrec, int msgkey)
{
	int i;
	for (i = 0 ; i < RECENT_CLIENT_MESSAGES_TO_TRACK ; i++)
	{
		if (qrec->client_message_keys[i] == msgkey)
			return 1;
	}
	qrec->cur_message_key = (qrec->cur_message_key + 1) % RECENT_CLIENT_MESSAGES_TO_TRACK;
	qrec->client_message_keys[qrec->cur_message_key] = msgkey;
	return 0;
}
