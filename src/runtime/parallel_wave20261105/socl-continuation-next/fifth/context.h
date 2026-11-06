typedef unsigned char u8;
typedef unsigned long u32;
typedef struct {u32 state[4],low,high;u8 buffer[64];} Md5View;
extern const u8 native_data_020de898[64];
extern const u32 native_data_020de918[64];
extern void native_fn_02092ca8(u32 *,u8 *,unsigned int);
extern void native_main_02092cb8(Md5View *,u8 *);
