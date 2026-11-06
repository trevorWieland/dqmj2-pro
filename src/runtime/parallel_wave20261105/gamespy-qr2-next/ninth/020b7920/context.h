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
#define QR2_SPLITNUM_FINALFLAG	(1<<7)
gsi_bool qr_build_split_query_reply(qr2_t qrec, qr2_buffer_t buf, struct QRSplitQueryProgress* progress);
void qr_build_query_reply(qr2_t qrec, qr2_buffer_t buf, int serverkeycount, uchar *serverkeys, int playerkeycount, uchar *playerkeys, int teamkeycount, uchar *teamkeys);
extern int sendto(SOCKET,const char*,int,int,const struct sockaddr*,int);
#define gsi_is_false(x) ((x)==gsi_false)
#define gsi_is_true(x) ((x)!=gsi_false)
typedef unsigned char u8;
static inline void*copybytes(void*dst,const void*src,u32 n){u8*d=dst;const u8*s=src;if(n==4){d[0]=s[0];d[1]=s[1];d[2]=s[2];d[3]=s[3];}else if(n==2){d[0]=s[0];d[1]=s[1];}else if(n)do{*d++=*s++;}while(--n);return dst;}
#define memcpy copybytes
extern const char native_data_020e25ac[8];
extern const char native_data_020e25b4[1];
extern const char* native_data_020e277c[255];
