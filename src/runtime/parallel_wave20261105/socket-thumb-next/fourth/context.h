typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ThreadView ThreadView;
typedef struct SocketView SocketView;
struct SocketView { ThreadView *owner0; u32 kind4; u8 state8; u8 mode9; u16 localA; u32 opaqueC; u32 tick10; u32 localIP14; u16 remote18; u16 remote1A; u32 address1C; u32 address20; u32 word24; u32 word28; u8 opaque2C[12]; s32 (*callback38)(u8 *,u32,SocketView *); u32 capacity3C; u8 *buffer40; u32 size44; u8 opaque48[24]; u32 word60; };
struct ThreadView { u8 opaque0[104]; ThreadView *next68; u8 opaque6C[56]; SocketView *socketA4; };
typedef struct Singleton { u32 opaque0; ThreadView *current4; ThreadView *list8; } Singleton;
typedef struct IPHeader { u8 opaque0[12]; u16 sourceC[2]; u16 destination10[2]; } IPHeader;
typedef struct DatagramHeader { u16 source0; u16 destination2; u16 bytes4; u16 checksum6; } DatagramHeader;
extern Singleton native_data_020e33e4;
extern u32 native_fn_0208bbac(const void *,u32,const void *,u32);
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32);
extern void native_fn_0200698c(ThreadView *);
extern void native_fn_02008e0c(const void *,void *,u32);
static inline u16 host16(u16 value){return (u16)((value>>8)|(value<<8));}
static inline u32 host32(u16 *p){return ((u32)host16(p[0])<<16)|host16(p[1]);}
#define AT(T,F) ((u32)&((T *)0)->F)
typedef char WordLayout[(sizeof(u32)==4 && sizeof(void *)==4)?1:-1];
typedef char SocketLayout[(sizeof(SocketView)==100 && AT(SocketView,state8)==8 && AT(SocketView,localA)==10 && AT(SocketView,localIP14)==20 && AT(SocketView,remote18)==24 && AT(SocketView,address1C)==28 && AT(SocketView,callback38)==56 && AT(SocketView,capacity3C)==60 && AT(SocketView,buffer40)==64 && AT(SocketView,size44)==68)?1:-1];
typedef char ThreadLayout[(sizeof(ThreadView)==168 && AT(ThreadView,next68)==104 && AT(ThreadView,socketA4)==164)?1:-1];
typedef char SingletonLayout[(sizeof(Singleton)==12 && AT(Singleton,current4)==4 && AT(Singleton,list8)==8)?1:-1];
typedef char HeaderLayout[(sizeof(IPHeader)==20 && sizeof(DatagramHeader)==8 && AT(IPHeader,sourceC)==12 && AT(IPHeader,destination10)==16 && AT(DatagramHeader,checksum6)==6)?1:-1];
