typedef unsigned int u32;
typedef signed int s32;
s32 native_ov001_021e88a4(s32 value, s32 factor, u32 width) {
    s32 product;
    s32 bias;
    u32 maximum;
    s32 result;
    product = (s32)((u32)value * (u32)factor);
    bias = product < 0 ? -2048 : 2048;
    maximum = 1U << (width * 8 - 1);
    result = (s32)((u32)product + (u32)bias) / 4096;
    maximum = (maximum >> 1) - 1;
    if ((s32)maximum <= result) result = (s32)maximum;
    return result;
}
