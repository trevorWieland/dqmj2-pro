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
typedef signed short s16;typedef unsigned long long u64;
typedef u8 CPSMacAddress[6];
typedef struct{u32 ip;CPSMacAddress mac;u16 when;}CPSArpCache;
typedef struct{u8 opaque0[40];volatile u32 putpnt;u32 opaque44;volatile u32 getpnt;u8 opaque52[28];u32 myip;void*volatile recvthread;u8*buf;volatile u32 buflen;}CPSGlobalView;
typedef struct{u32 opaque0;void*current;}ThreadInfoView;
extern CPSGlobalView native_data_021cfcf8;
extern ThreadInfoView native_data_020e33e4;
extern CPSMacAddress native_data_021d01e0,native_data_020de7ac;
extern u8 native_data_020de7b4[8];
extern CPSArpCache native_data_021cfd78[8];
extern void native_fn_02008e0c(const void*,void*,u32);
extern void native_fn_02008d78(void*,u8,u32);
extern u32 native_fn_02007ff4(void),native_fn_02008008(u32);
extern u64 native_fn_02007a9c(void);
extern void native_fn_0208bce8(u8*,u32,u8*,u32);
extern u32 native_fn_0208bbe8(u32),native_fn_0208bc58(u32),native_fn_0208bc30(u32),native_fn_0208bc18(u32);
extern CPSMacAddress*native_fn_0208bf10(u32),*native_fn_0208c038(u32);
extern void native_fn_0208bd24(u8*,u8*,u8*,u32,u8*,u32);
extern int native_fn_020068c0(void*);
extern void native_fn_0200698c(void*),native_fn_020068d4(void*);
static inline u32 tick(void){return(u32)(native_fn_02007a9c()>>16);}
#define G native_data_021cfcf8
#define ARP native_data_021cfd78

void native_main_0208bd24(u8*srcAddr,u8*dstAddr,u8*buf1,u32 size1,u8*buf2,u32 size2);
