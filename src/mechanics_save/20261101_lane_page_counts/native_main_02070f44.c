typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
#define FIELD(value,type,offset) (*(type)((u8 *)(value)+(offset)))
extern u8 native_data_021c4f60[];
u32 native_main_02070f44(void) {
    s8 result;
    s32 count;
    if(FIELD(native_data_021c4f60,s8 *,0x2F)!=0)return 1;
    count=FIELD(native_data_021c4f60,s32 *,0x14);
    result=count/14;
    if(count%14)result++;
    if(result==0)result++;
    return (u32)result;
}
