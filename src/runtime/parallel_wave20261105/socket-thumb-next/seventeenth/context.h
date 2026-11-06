typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned long u32;
typedef struct SocView {u8 opaque0[44];u16 window2C;u16 mss2E;} SocView;
typedef struct ThreadView {u8 opaque0[164];SocView *specificA4;} ThreadView;
typedef struct KernelView {u32 opaque0;ThreadView *current4;} KernelView;
typedef struct CpsConfigView {u8 opaque0[36];u32 mss24;} CpsConfigView;
extern KernelView native_data_020e33e4;
extern CpsConfigView native_data_021d1550;
extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32);
extern int native_fn_02026144(int,int);
static inline int minimum(int a,int b){return a<=b?a:b;}
#define AT(T,F) ((u32)&((T *)0)->F)
typedef char Layout[(sizeof(u32)==4 && sizeof(int)==4 && sizeof(void *)==4 && sizeof(SocView)==48 && AT(SocView,window2C)==44 && AT(SocView,mss2E)==46 && sizeof(ThreadView)==168 && AT(ThreadView,specificA4)==164 && sizeof(KernelView)==8 && AT(KernelView,current4)==4 && sizeof(CpsConfigView)==40 && AT(CpsConfigView,mss24)==36)?1:-1];
