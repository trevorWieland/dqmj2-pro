typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 native_data_021c4fe4[32];
u32 native_main_020707c4(void) {
    s32 nextIndex;
    s8 count;
    s8 index;
    u8 *pointer;
    count=0;
    pointer=native_data_021c4fe4;
    index=count;
loop:
    if(*pointer==0)return (u32)count;
    nextIndex=index+1;
    count++;
    index=(s8)nextIndex;
    pointer++;
    if(index<32)goto loop;
    return (u32)count;
}
