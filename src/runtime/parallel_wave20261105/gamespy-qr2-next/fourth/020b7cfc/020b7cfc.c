#include "context.h"
void native_main_020b7cfc(qr2_t qrec, qr2_buffer_t buf, uchar *qdata, int len, struct sockaddr* sender)
{
	uchar serverkeycount;
	uchar playerkeycount;
	uchar teamkeycount;
	uchar exflags = 0;
	uchar *serverkeys = NULL;
	uchar *playerkeys = NULL;
	uchar *teamkeys = NULL;
	if (len < 3)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"Discarding invalid query (too short#1: %d bytes total)\r\n", len);
		return;
	}
	serverkeycount = qdata[0];
	qdata++;
	len--;
	if (serverkeycount != 0 && serverkeycount != 0xFF)
	{
		serverkeys = qdata;
		qdata += serverkeycount;
		len -= serverkeycount;
	}
	if (len < 2)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"Discarding invalid query (too short#2: %d bytes remain)\r\n", len);
		return;
	}
	playerkeycount = qdata[0];
	qdata++;
	len--;
	if (playerkeycount != 0 && playerkeycount != 0xFF)
	{
		playerkeys = qdata;
		qdata += playerkeycount;
		len -= playerkeycount;
	}
	if (len < 1)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"Discarding invalid query (too short#3: %d bytes remain)\r\n", len);
		return;
	}
	teamkeycount = qdata[0];
	qdata++;
	len--;
	if (teamkeycount != 0 && teamkeycount != 0xFF)
	{
		teamkeys = qdata;
		qdata += teamkeycount;
		len -= teamkeycount;
	}
	if (len < 0)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_WarmError,
			"Discarding invalid query (too short#4: %d bytes remain)\r\n", len);
		return;
	}
	if (len > 0)
	{
		exflags = qdata[0];
		len--;
	}
	if ((exflags & QR2_EXFLAG_SPLIT)==QR2_EXFLAG_SPLIT)
	{
		struct QRSplitQueryProgress progress;
		progress.mCurPacketNum = 0;
		progress.mCurKeyType = key_server;
		progress.mCurKeyIndex = 0;
		progress.mCurSubCount = 0;
		progress.mCurSubIndex = 0;
		progress.mKeyBuffer.numkeys = 0;
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
			"Building query reply (split packet supported)\r\n");
		while (gsi_true == native_fn_020b7b00(qrec, buf, &progress))
		{
			native_fn_020a8c34(qrec->hbsock, buf->buffer, buf->len, 0, sender, sizeof(struct sockaddr_in));
			buf->len = 5;
			if (progress.mCurPacketNum > QR2_SPLITNUM_MAX)
				return;
		}
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
				"Finished split query reply (%d packets)\r\n", progress.mCurPacketNum);
	}
	else
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Network, GSIDebugLevel_Comment,
			"Building query reply (single packet)\r\n");
		native_fn_020b7ac8(qrec, buf, serverkeycount, serverkeys, playerkeycount, playerkeys, teamkeycount, teamkeys);
		native_fn_020a8c34(qrec->hbsock, buf->buffer, buf->len, 0, sender, sizeof(struct sockaddr_in));
	}
	GSI_UNUSED(sender);
}
