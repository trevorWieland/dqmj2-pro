typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned long u32;
typedef signed long s32;
typedef struct SendView SendView;
typedef struct SocketView {u8 cps0[100];void *recv64;SendView *send68;volatile s32 result6C;volatile s16 state70;s8 block72;s8 mode73;u8 opaque74[12];} SocketView;
struct SendView {u8 opaque0[268];SocketView *executor10C;};
typedef struct CommandView {int (*handler0)(void *);SocketView *socket4;void *response8;s8 modeC;s8 blockD;u8 padE[2];} CommandView;
extern int native_fn_02090294(SocketView *);
extern int native_fn_020902b4(SocketView *);
extern CommandView *native_fn_0208ebd8(int (*)(void *),SocketView *,s32);
extern int native_fn_0208ecb0(SocketView *,CommandView *);
extern int native_fn_0208fc70(void *);
extern int native_fn_0208fd4c(void *);
extern void native_fn_0208d8e8(void);
extern int native_fn_0208ec1c(void *,void *);
extern int native_fn_0208ec50(SocketView *,CommandView *);
static inline int state(SocketView *socket,u16 mask){return (s32)socket->state70&(s32)mask;}
static inline int created(SocketView *socket){return socket && state(socket,1);}
static inline int tcp(SocketView *socket){return socket->mode73==0 || socket->mode73==4;}
#define AT(T,F) ((u32)&((T *)0)->F)
typedef char Layout[(sizeof(u32)==4 && sizeof(s32)==4 && sizeof(void *)==4 && sizeof(SocketView)==128 && AT(SocketView,send68)==104 && AT(SocketView,state70)==112 && AT(SocketView,block72)==114 && AT(SocketView,mode73)==115 && sizeof(SendView)==272 && AT(SendView,executor10C)==268 && sizeof(CommandView)==16 && sizeof(((CommandView *)0)->response8)==4 && sizeof(((SocketView *)0)->state70)==2 && sizeof(((SocketView *)0)->block72)==1 && AT(CommandView,response8)==8)?1:-1];
