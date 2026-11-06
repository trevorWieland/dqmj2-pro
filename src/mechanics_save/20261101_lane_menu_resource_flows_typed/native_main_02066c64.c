typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
#define FIELD(p,t,n) (*(t *)((u8 *)(p)+(n)))
extern u8 native_data_021c36e8[];
extern u8 native_data_020de210[];
extern u8 native_data_020de224[];
extern u32 native_fn_ov000_021df1f0(void);
extern u32 native_fn_ov000_021df220(u32,s8 *,u8 *,u8 *);
extern int native_fn_0201d444(u8 *,const u8 *,...);
extern u32 native_fn_0203cc2c(u32,u32);

u32 native_main_02066c64(u32 arg0) {
    u8 path[17];
    s8 prefix;
    u8 first;
    u8 second;
    u32 mode;
    u32 handle;
    u32 index;
    u32 result;
    index=arg0;
    result=0;
    mode=FIELD(native_data_021c36e8,u32,12);
    if (mode==0) {
        if(index==255)index=native_fn_ov000_021df1f0();
        native_fn_ov000_021df220(index,&prefix,&first,&second);
        native_fn_0201d444(path,native_data_020de210,prefix,first,second);
    } else {
        native_fn_0201d444(path,native_data_020de224,(const u8 *)mode);
    }
    handle=native_fn_0203cc2c((u32)path,1);
    FIELD(native_data_021c36e8,u32,4)=handle;
    if(handle!=0 && *(u32 *)handle==0x54434E45)result=1;
    return result;
}
