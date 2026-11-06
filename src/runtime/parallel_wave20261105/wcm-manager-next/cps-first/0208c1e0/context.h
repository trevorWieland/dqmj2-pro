typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef signed long s32;
#define NULL ((void*)0)
static inline u16 CPS_htons(u16 data){return(u16)((data>>8)|(data<<8));}
static inline u32 CPS_htonl(u32 data){u32 tmp;tmp=((data>>8)&0x00ff00ff)|((data<<8)&0xff00ff00);return(tmp>>16)|(tmp<<16);}
#define CPS_USHORT2_HOST(p) (*(u16*)(p))
#define CPS_GETUSHORT1(p) ((u16)(((u8*)(p))[0]<<8|((u8*)(p))[1]))
#define CPS_SETUSHORT2(p,v) CPS_USHORT2_HOST(p)=CPS_htons((u16)(v))
#define CPS_SETULONG2(p,v) do{CPS_SETUSHORT2(p,(u32)(v)>>16);CPS_SETUSHORT2((p)+2,v);}while(0)
extern u32 native_fn_0208bb08(u8*,u32,u32);
extern u16 native_fn_0208bb84(u16);
typedef struct OSThread OSThread;
typedef struct{u32 size;u8*data;}CPSSocBuf;
typedef struct _CPSSoc{OSThread*thread;u32 block_type;u8 state;u8 ssl;u16 local_port;void*con;u32 when;u32 local_ip_real;u16 remote_port;u16 remote_port_bound;u32 remote_ip;u32 remote_ip_bound;u32 ackno;u32 seqno;u16 remote_win;u16 remote_mss;u32 remote_ackno;u32 ackrcvd;int(*udpread_callback)(u8*,u32,struct _CPSSoc*);CPSSocBuf rcvbuf;u32 rcvbufp;CPSSocBuf sndbuf;CPSSocBuf linbuf;CPSSocBuf outbuf;u32 outbufp;}CPSSoc;
typedef struct{u8 opaque0[0x50];u32 my_ip;}CPSGlobalView;
extern CPSGlobalView native_data_021cfcf8;
extern u8 native_data_020de7b4[8],native_data_021d01e0[6];
extern u16 native_fn_0208bb98(u8*,u32);
extern u32 native_fn_0208bc58(u32);
extern void native_fn_0208c140(u8*,u32,u8*,u32,u32,u16);
extern void native_fn_0208bd24(u8*,u8*,u8*,u32,u8*,u32);
extern void native_fn_02008e0c(const void*,void*,u32);
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern void native_fn_0208c1e0(u8*,u32,u8*,u32,u32,u32);
extern void native_fn_0208c2b4(u8*,u32,u8*,u32,u32,u8);
#define CPSMyIp native_data_021cfcf8.my_ip

void native_main_0208c1e0(u8*hdr,u32 hdr_len,u8*body,u32 body_len,u32 ip_to,u32 offset);
