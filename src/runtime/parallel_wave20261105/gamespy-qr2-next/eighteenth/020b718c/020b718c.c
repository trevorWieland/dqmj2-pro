#include "context.h"
qr2_error_t native_main_020b718c(qr2_t *qrec, SOCKET s, int boundport, const char *gamename, const char *secret_key,
					 int ispublic, int natnegotiate,
					 qr2_serverkeycallback_t server_key_callback,
					 qr2_playerteamkeycallback_t player_key_callback,
					 qr2_playerteamkeycallback_t team_key_callback,
					 qr2_keylistcallback_t key_list_callback,
					 qr2_countcallback_t playerteam_count_callback,
					 qr2_adderrorcallback_t adderror_callback,
					 void *userdata)
{
	char hostname[64];
	int ret;
	int i;
	qr2_t cr;
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_StackTrace,
		"qr2_init_socket()\r\n");
	if (qrec == NULL)
	{
		cr = &native_data_020e17a0;
	}
	else
	{
		*qrec = (qr2_t)native_fn_020a927c(sizeof(struct qr2_implementation_s));
		cr = *qrec;
	}
	native_fn_0201d608((unsigned int)native_fn_020a8ef8());
	native_fn_0201d6b8(cr->gamename,gamename);
	native_fn_0201d6b8(cr->secret_key,secret_key);
	cr->qport = boundport;
	cr->lastheartbeat = 0;
	cr->lastka = 0;
	cr->hbsock = s;
	cr->listed_state = 1;
	cr->udata = userdata;
	cr->server_key_callback = server_key_callback;
	cr->player_key_callback = player_key_callback;
	cr->team_key_callback = team_key_callback;
	cr->key_list_callback = key_list_callback;
	cr->playerteam_count_callback = playerteam_count_callback;
	cr->adderror_callback = adderror_callback;
	cr->nn_callback = NULL;
	cr->cm_callback = NULL;
	cr->cdkeyprocess = NULL;
	cr->ispublic = ispublic;
	cr->read_socket = 0;
	cr->nat_negotiate = natnegotiate;
	cr->publicip = 0;
	cr->publicport = 0;
	cr->pa_callback = NULL;
	cr->userstatechangerequested = 0;
	cr->backendoptions = 0;
	for (i = 0 ; i < REQUEST_KEY_LEN ; i++)
		cr->instance_key[i] = (char)(native_fn_0201d5d4() % 0xFF);
	for (i = 0 ; i < RECENT_CLIENT_MESSAGES_TO_TRACK ; i++)
		cr->client_message_keys[i] = -1;
	cr->cur_message_key = 0;
	native_fn_0201b208(cr->ipverify, 0, sizeof(cr->ipverify));
	native_fn_020b75cc();
	if (ispublic)
	{
		int override = native_data_021d2ee0[0];
		if(!override)
			native_fn_0200616c(hostname, native_data_020e2534, gamename);
		ret = native_fn_020b760c(override?native_data_021d2ee0:hostname, MASTER_PORT, &(cr->hbaddr), NULL);
		if (ret == 1)
		{
			gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
				"%s resolved to %s\r\n", override?native_data_021d2ee0:hostname, inet_ntoa(cr->hbaddr.sin_addr));
		}
		else
		{
			gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_HotError,
				"Failed on DNS lookup for %s \r\n", override?native_data_021d2ee0:hostname);
		}
	}
	else
		ret = 1;
	if (!ret)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_HotError,
			"qr2_init_socket() returned failed (DNS error)\r\n");
		return e_qrdnserror;
	}
	else
	{
		return e_qrnoerror;
	}
}
