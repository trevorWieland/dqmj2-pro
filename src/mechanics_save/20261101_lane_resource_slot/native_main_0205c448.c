typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
#define WORD(p,n) (*(u32 *)((u8 *)(p)+(n)))
extern u8 native_data_02102e2c[];
extern void native_fn_02008c14(u32,void *,u32);
u32 native_main_0205c448(void) {
    s32 index;
    u32 result;
    u8 *row;
    result=0;
    row=native_data_02102e2c;
    index=0;
loop:
    if(WORD(row,4)==0) {
        result=index*172+(s32)native_data_02102e2c;
        native_fn_02008c14(0,(void *)result,172);
    } else {
        index++;
        row+=172;
        if(index<32)goto loop;
    }
    return result;
}
