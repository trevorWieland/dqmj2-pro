typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
#define WORD(p,n) (*(u32 *)((u8 *)(p)+(n)))
extern u32 native_fn_02061944(void);
extern int native_fn_0201d444(u8 *,const u8 *,...);
extern u32 native_fn_0205ff80(u32);
extern u32 native_fn_0205ff9c(void);
extern u32 native_fn_02065730(u32,u32,u32,u32,u32);

extern u8 native_data_020de328[];
extern u32 native_fn_02065d28(u32);
extern u32 native_fn_0206e148(void);
void native_main_0206df70(void) {
    u8 path[32];
    u32 value;
    u8 *context;
    context=(u8 *)native_fn_02061944();
    native_fn_0201d444(path,native_data_020de328);
    native_fn_0205ff80((u32)path);
    value=native_fn_02065d28(61);
    value=WORD(context,0x260)-value;
    WORD(context,0x260)=value;
    native_fn_02065730((u32)(context+16),61,0,1,value);
    native_fn_0205ff9c();
    native_fn_0206e148();
}
