typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;
typedef unsigned long long u64;
typedef long long s64;
typedef struct {u32 addr;} Address;
typedef struct {s32 fd;s16 events,revents;} PollEntry;
typedef struct {u8 prefix[0x70];volatile s16 state;s8 block,mode;} SocketPrefix;
typedef struct SslConnection SslConnection;
extern u32 native_fn_0209009c(const char *);
extern void native_fn_02008e0c(const void *,void *,u32);
extern void native_fn_020907e4(u32,u8 *);
extern s32 native_fn_020061ac(char *,u32,const char *,...);
extern const char native_data_020de81c[12];
extern s32 native_fn_02090138(s32);
extern void native_fn_02006b7c(u32);
extern s32 native_fn_02090294(SocketPrefix *);
extern s32 native_fn_020908f0(SocketPrefix *,SslConnection *);
static inline s32 socket_tcp(SocketPrefix *s){return s->mode==0 || s->mode==4;}
static inline s32 socket_state(SocketPrefix *s,u16 mask){return (s32)s->state & (s32)mask;}
static inline s32 socket_created(SocketPrefix *s){return s && socket_state(s,1);}
static inline s32 socket_connecting(SocketPrefix *s){return socket_state(s,2);}
extern s32 native_main_0209075c(const char *,Address *);
extern const char *native_main_02090794(s32,const void *,char *,u32);
extern s32 native_main_020907f4(PollEntry *,u32,u64);
extern s32 native_main_0209088c(s32,SslConnection *);
typedef struct {u32 state[4],low,high;u8 buffer[64];} Md5View;
typedef struct {u32 state[5],high,low;u8 buffer[64];} Sha1View;
typedef struct {u8 x,y,state[256];} Rc4View;
extern void native_fn_02092cb8(Md5View *,const u8 *);
extern void native_fn_02093180(Sha1View *,const u8 *);
extern void native_main_0209302c(Md5View *,const u8 *,u32);
extern void native_main_020936f4(Sha1View *,const u8 *,u32);
extern void native_main_020937dc(Rc4View *,const u8 *,s32);
extern void native_main_02093824(Rc4View *,u8 *,s32);
extern void native_fn_02092c98(u8 *,const u32 *,u32);
extern void native_fn_02093128(u8 *,const u32 *,u32);
extern void native_fn_0209302c(Md5View *,const u8 *,u32);
extern void native_fn_020936f4(Sha1View *,const u8 *,u32);
extern void native_main_020930ac(Md5View *,u8 *);
extern void native_main_02093774(Sha1View *,u8 *);
extern const u8 native_data_020de8d8[64];
extern const u8 native_data_020dea18[64];
