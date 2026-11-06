typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u32 native_host_arm7_runtime_word_0380fff4;

u32 native_arm7_main_027ea584(void) {
    switch (*(u16 *)(native_host_arm7_runtime_word_0380fff4 + 0x330)) {
    case 0:
        if ((*(u16 *)(native_host_arm7_runtime_word_0380fff4 + 0x3a4) & 1) != 0) {
            return 10;
        }
        break;
    case 1:
        return 10;
    }
    return 20;
}
