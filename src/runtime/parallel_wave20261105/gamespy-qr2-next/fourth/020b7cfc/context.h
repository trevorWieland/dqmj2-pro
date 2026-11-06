#include "types.h"
#define MAX_DATA_SIZE 1400
typedef unsigned char uchar;
struct qr2_keybuffer_s
{
	uchar keys[MAX_REGISTERED_KEYS];
	int numkeys;
};
struct qr2_buffer_s
{
	char buffer[MAX_DATA_SIZE];
	int len;
};
#define AVAILABLE_BUFFER_LEN(a) (MAX_DATA_SIZE - (a)->len)
#define MAX_CHALLENGE 64
uchar encode_ct ( uchar c );
void gs_encrypt ( uchar *key, int key_len, uchar *buffer_ptr, int buffer_len );
void gs_encode ( uchar *ins, int size, uchar *result );
struct QRSplitQueryProgress
{
	qr2_key_type mCurKeyType;
	int mCurPacketNum;
	int mCurKeyIndex;
	int mCurSubCount;
	int mCurSubIndex;
	struct qr2_keybuffer_s mKeyBuffer;
};
#define QR2_EXFLAG_SPLIT		(1<<0)
#define QR2_SPLITNUM_MAX		7
gsi_bool native_fn_020b7b00(qr2_t qrec, qr2_buffer_t buf, struct QRSplitQueryProgress* progress);
void native_fn_020b7ac8(qr2_t qrec, qr2_buffer_t buf, int serverkeycount, uchar *serverkeys, int playerkeycount, uchar *playerkeys, int teamkeycount, uchar *teamkeys);
extern int native_fn_020a8c34(SOCKET,const char*,int,int,const struct sockaddr*,int);
