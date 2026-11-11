typedef unsigned char u8;
typedef unsigned int u32;

void native_main_020907e4(u32 value, u8 *out) {
    out[0] = (u8)(value >> 24);
    out[1] = (u8)(value >> 16);
    out[2] = (u8)(value >> 8);
    out[3] = (u8)value;
}
