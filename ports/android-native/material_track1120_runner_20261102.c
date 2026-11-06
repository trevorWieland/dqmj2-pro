#include <stdint.h>
#include <stdio.h>

typedef struct NNSG3dResMatCAnm_ NNSG3dResMatCAnm;
typedef struct NNSG3dResTexSRTAnm_ NNSG3dResTexSRTAnm;
typedef char fixed_width[(sizeof(unsigned int) == 4 && sizeof(int) == 4) ? 1 : -1];
extern uint16_t native_main_02033930(const NNSG3dResMatCAnm *, unsigned int, unsigned int);
extern uint16_t native_main_02033a98(const NNSG3dResMatCAnm *, unsigned int, unsigned int);
extern int native_main_02033d48(const NNSG3dResTexSRTAnm *, unsigned int, unsigned int, unsigned int);
extern unsigned int native_main_02033e48(const NNSG3dResTexSRTAnm *, unsigned int, unsigned int, unsigned int);
static union {
    uint32_t alignment;
    uint8_t bytes[16384];
} page;

static int read_exact(void *destination, size_t bytes) {
    return fread(destination, 1, bytes, stdin) == bytes;
}

static int write_exact(const void *source, size_t bytes) {
    return fwrite(source, 1, bytes, stdout) == bytes;
}

int main(void) {
    uint32_t count, index;
    if (!read_exact(&count, 4) || count > 4096) return 81;
    for (index = 0; index < count; ++index) {
        uint32_t h[5], result;
        if (!read_exact(h, sizeof(h)) || h[1] != 0x02400000 || !read_exact(page.bytes, sizeof(page.bytes))) return 82;
        switch (h[0]) {
        case 0x02033930: result = native_main_02033930((void *)page.bytes, h[2], h[3]);break;
        case 0x02033A98: result = native_main_02033a98((void *)page.bytes, h[2], h[3]);break;
        case 0x02033D48: result = (uint32_t)native_main_02033d48((void *)page.bytes, h[2], h[3], h[4]);break;
        case 0x02033E48: result = native_main_02033e48((void *)page.bytes, h[2], h[3], h[4]);break;
        default: return 83;
        }
        if (!write_exact(&index, 4) || !write_exact(&result, 4) || !write_exact(page.bytes, sizeof(page.bytes))) return 84;
    }
    if (fgetc(stdin) != EOF || ferror(stdin) || fflush(stdout)) return 85;
    return 0;
}
