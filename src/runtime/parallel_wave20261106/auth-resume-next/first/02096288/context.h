typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;typedef int BOOL;
typedef union{u32 us32;u8 us8[4];}U4B;
typedef struct{u32 state[4];unsigned long long length;union{u32 buffer32[16];u8 buffer8[64];};}MATHMD5Context;
typedef struct{const char*shmask0;const char*mask0;const char*shmask1;const char*mask1;}ShopKeys;
extern ShopKeys native_data_020dea70;
extern const char native_data_020dead8[9];
extern const u8 native_data_020dc4a3[24],native_data_020dc4bc[13],native_data_020dc4cc[16];
void native_main_02096174(const char*,u8*);
void native_main_020961c8(const char*,u8*);
void native_main_02096258(const u8*,u8*);
void native_main_02096288(const u8*,u8*);
long native_main_0209636c(u8);
int native_main_020963b4(const char*,u8*,u32,u32);
void native_fn_02008e0c(const void*,void*,u32);
int native_fn_0201b248(const void*,const void*,u32);
void native_fn_0200cad0(MATHMD5Context*);
void native_fn_0200cb10(MATHMD5Context*,const void*,u32);
void native_fn_0200cbd8(void*,MATHMD5Context*);
void native_fn_020961c8(const char*,u8*);
int native_fn_020963b4(const char*,u8*,u32,u32);
long native_fn_0209636c(u8);
#define decodeSSID native_fn_020961c8
#define db64 native_fn_020963b4
#define codetovalue native_fn_0209636c
#define MI_CpuCopy8 native_fn_02008e0c
#define memcmp native_fn_0201b248
#define NINTENDO_SHOP_SSID native_data_020dead8
#define NINTENDO_SHOP_SSID_LENGTH 8
#define SSID_LENGTH 24
#define WEPKEY_LENGTH 13
#define SHMASKkey0 native_data_020dea70.shmask0
#define SHMASKkey1 native_data_020dea70.shmask1
#define MASKkey0 native_data_020dea70.mask0
#define MASKkey1 native_data_020dea70.mask1
#define CONV_BYTE_TABLE native_data_020dc4bc
#define CONV_4BIT_TABLE native_data_020dc4cc
static inline void MATH_MD5Init(MATHMD5Context*c){native_fn_0200cad0(c);}
static inline void MATH_MD5Update(MATHMD5Context*c,const void*p,u32 n){native_fn_0200cb10(c,p,n);}
static inline void MATH_MD5GetHash(MATHMD5Context*c,void*p){native_fn_0200cbd8(p,c);}
