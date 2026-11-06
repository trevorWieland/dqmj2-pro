typedef unsigned char u8;
typedef unsigned int u32;
extern void native_fn_02008e0c(const void *,void *,u32);
extern u8 native_data_020fade0[];
void native_main_02047ff0(const u8 *input,u32 length,u32 offset) {
    u8 *destination=native_data_020fade0+offset;
    native_fn_02008e0c(input,destination,length);
    destination[length]=0xE3;
    (native_data_020fade0+1+offset)[length]=0x1B;
}
