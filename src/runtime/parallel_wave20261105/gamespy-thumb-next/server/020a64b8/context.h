typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {u32 publicip;u16 publicport;u32 privateip;u16 privateport;u32 icmpip;u8 state,flags;void *keyvals;u32 updatetime,challenge;void *next;u8 bitmap;} Server;
extern const char native_data_020e0318[];
extern const u16 native_data_020d8e04[128];
int native_fn_0201d800(const char *,const char *);
int native_fn_020a64d0(Server *);
const char *native_fn_020a5fe4(Server *,const char *,const char *);
int native_fn_0201f274(const char *);
static inline int digit(int c){return c<0 || c>=128 ? 0:(native_data_020d8e04[c]&8);}
typedef Server *SBServer;
typedef void *SBServerList;
typedef unsigned int goa_uint32;
typedef int gsi_bool;
#define gsi_false 0
#define gsi_true 1
#define SBTrue 1
#define NULL ((void *)0)
#define GS_ASSERT(x)
#define GSI_UNUSED(x) ((void)(x))
#define gsDebugFormat(...) ((void)0)
#define MULTIPLIER -1664117991
#define QR2_SPLITPACKET_NUMSTRING native_data_020e032c
#define QR2_SPLITPACKET_MAX 7
#define QR2_SPLITPACKET_FINAL 128
#define NUM_BUCKETS 8
#define NUM_CHAINS 4
extern char *native_data_021d2360;
extern const u8 native_data_020d8d04[128];
extern const char native_data_020e0320[],native_data_020e0324[],native_data_020e032c[];
typedef struct {const char *keys[2];} InvalidKeys;
extern const InvalidKeys native_data_020dc534;
typedef struct {const char *key,*value;} SBKeyValuePair;
int native_fn_02023f6c(const char *,const char *);
int native_fn_02023f60(const char *,const char *,u32);
u32 native_fn_0201d69c(const char *);
int native_fn_0200616c(char *,const char *,...);
void *memcpy(void *,const void *,u32);
char *native_fn_020a6140(char *,char);
int native_fn_020a6108(char *);
int native_fn_020b85a8(const char *);
void native_fn_020a5f98(SBServer,const char *,const char *);
int native_fn_020a6fa8(char *,int);
void *native_fn_020a927c(u32);
void native_fn_020a929c(void *);
void *native_fn_020a88ec(int,int,int,int (*)(const void *,int),int (*)(const void *,const void *),void (*)(void *));
int native_fn_020a64ac(const void *,int);
int native_fn_020a64b8(const void *,const void *);
void native_fn_020a6494(void *);
static inline int lower(int c){return c<0 || c>=128 ? c : native_data_020d8d04[c];}

