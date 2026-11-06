typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef signed char s8;
typedef unsigned long u32;
typedef signed long s32;
typedef struct UdpView {u8 opaque0[4];u16 size4;} UdpView;
typedef struct CpsView {u8 opaque0[8];u8 state8;u8 opaque9;u16 localA;u8 opaqueC[12];u16 remote18;u8 opaque1A[2];u32 peer1C;u8 opaque20[32];u8 *buffer40;u32 length44;} CpsView;
typedef struct RecvView {u8 opaque0[196];CpsView *specificC4;u8 opaqueC8[24];u8 mutexE0[24];volatile s32 consumedF8;u16 minFC;s8 noConsumeFE;u8 opaqueFF[5];UdpView *volatile out104;} RecvView;
typedef struct SocketView {u8 opaque0[8];u8 cpsState8;u8 opaque9[59];u32 received44;u8 opaque48[28];RecvView *recv64;void *send68;volatile s32 result6C;volatile s16 state70;s8 block72;s8 mode73;u16 local74;u16 remote76;u32 peer78;struct SocketView *next7C;} SocketView;
extern int native_fn_02090294(SocketView *);
extern s32 native_fn_020901e4(SocketView *);
extern s32 native_fn_0208f900(SocketView *);
extern int native_fn_0208f0a0(SocketView *);
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32);
static inline int state(SocketView *socket,u16 mask){return (s32)socket->state70&(s32)mask;}
static inline int created(SocketView *socket){return socket && state(socket,1);}
static inline int tcp(SocketView *socket){return socket->mode73==0 || socket->mode73==4;}
static inline int udp(SocketView *socket){return socket->mode73==1;}
static inline int block(SocketView *socket){return socket->block72==1;}
#define AT(T,F) ((u32)&((T *)0)->F)
typedef char WordLayout[(sizeof(u32)==4 && sizeof(s32)==4 && sizeof(int)==4 && sizeof(void *)==4)?1:-1];
typedef char SocketLayout[(sizeof(SocketView)==128 && AT(SocketView,cpsState8)==8 && AT(SocketView,received44)==68 && AT(SocketView,recv64)==100 && AT(SocketView,result6C)==108 && AT(SocketView,state70)==112 && AT(SocketView,mode73)==115 && AT(SocketView,remote76)==118 && AT(SocketView,peer78)==120)?1:-1];
typedef char RecvLayout[(sizeof(RecvView)==264 && AT(RecvView,consumedF8)==248 && AT(RecvView,out104)==260 && sizeof(UdpView)==6 && AT(UdpView,size4)==4)?1:-1];
extern int native_data_020de7d0;
extern int native_fn_0208f234(SocketView *,void *,int,u16 *,u32 *,s32,s32);
extern int native_fn_0208f2ac(SocketView *,void *,int,u16 *,u32 *,s32);
extern int native_fn_0208f2f8(SocketView *,void *,int,u16 *,u32 *);
extern u8 *native_fn_0208f3bc(SocketView *,s32 *,u16 *,u16 *,u32 *);
extern int native_fn_0208f404(SocketView *,void *,int,u16 *,u32 *);
extern int native_fn_0208f508(SocketView *);
extern int native_fn_0208f578(SocketView *,void *,int,u16 *,u32 *,s32);
extern void native_fn_02008e0c(const void *,void *,u32);
typedef char CpsLayout[(sizeof(CpsView)==72 && sizeof(((CpsView *)0)->peer1C)==4 && sizeof(((CpsView *)0)->localA)==2 && AT(CpsView,localA)==10 && AT(CpsView,remote18)==24 && AT(CpsView,peer1C)==28 && AT(CpsView,buffer40)==64 && AT(CpsView,length44)==68)?1:-1];
typedef char ReceiveFields[(AT(RecvView,specificC4)==196 && AT(RecvView,mutexE0)==224 && AT(RecvView,noConsumeFE)==254)?1:-1];
