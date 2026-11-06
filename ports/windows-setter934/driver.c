typedef unsigned char u8;
typedef unsigned int u32;
__declspec(dllimport) void __stdcall ExitProcess(u32);
u8 native_data_ov000_0223142c[0x800];
extern u32 native_ov000_021df200(u32);
static const u32 upperWords[7] = {0U,0x100U,0x8000U,0x10000U,0x7FFF0000U,0xFFFF0000U,0xFFFFFF00U};
void entry(void) {
    u32 upper;
    u32 low;
    u32 value;
    u32 result;
    u32 failures = 0;
    for (upper = 0; upper < 7; upper++) {
        for (low = 0; low < 256; low++) {
            value = upperWords[upper] | low;
            native_data_ov000_0223142c[0x7BF] = 0x5A;
            native_data_ov000_0223142c[0x7C0] = (u8)(low ^ 0xA5);
            native_data_ov000_0223142c[0x7C1] = 0xA5;
            result = native_ov000_021df200(value);
            if (result != value || native_data_ov000_0223142c[0x7C0] != low || native_data_ov000_0223142c[0x7BF] != 0x5A || native_data_ov000_0223142c[0x7C1] != 0xA5)
                failures++;
        }
    }
    ExitProcess(failures);
}
