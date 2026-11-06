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
void native_fn_020b7678 ( uchar *a, uchar *b );
