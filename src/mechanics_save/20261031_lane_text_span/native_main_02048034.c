typedef unsigned char u8;
typedef unsigned int u32;
extern void native_fn_02047ff0(const u8 *,u32,u32);
u32 native_main_02048034(const u8 *input,u32 offset) {
    u32 length;
    const u8 *cursor;
    u32 index;
    u32 limit;
    length=0;
    cursor=input;
    index=0;
    limit=128U-offset;
    if(limit!=0) {
        do {
        if(*cursor==0 || (*cursor==0xE3 && cursor[1]==0x1B)) {
            length=index;
            break;
        }
        index++;
        cursor++;
        } while(index<limit);
    }
    native_fn_02047ff0(input,length,offset);
    return length;
}
