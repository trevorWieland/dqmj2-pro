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
