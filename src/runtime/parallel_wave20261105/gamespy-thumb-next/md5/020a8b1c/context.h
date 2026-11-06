typedef unsigned char u8;
typedef unsigned int u32;
typedef struct{u32 state[4],count[2];u8 buffer[64];} MD5_CTX;
extern const char native_data_020dc53c[16];
void native_fn_0209426c(MD5_CTX*);
void native_fn_02094274(MD5_CTX*,u8*,u32);
void native_fn_0209427c(u8*,MD5_CTX*);
void native_fn_020a8ae0(u8*,char*);
#define MD5Init native_fn_0209426c
#define MD5Update native_fn_02094274
#define MD5Final native_fn_0209427c
#define MD5Print native_fn_020a8ae0
#define hex_digits native_data_020dc53c
