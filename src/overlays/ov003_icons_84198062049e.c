typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 first; u32 second; u16 reserved; u8 value; u8 layer; } Cell;

extern char data_ov003_021e0290[];
extern char data_ov003_021e02a4[];
extern char data_ov003_021e02b4[];
extern u32 func_02044cdc(u32);
extern u32 func_02072f48(u32);
extern u16 func_02061de4(Cell *, u32, u32, u32, u32);
extern void func_0201d444(void *, const void *, ...);
extern u8 *func_0203cf20(void *, void *, u32);
extern void func_020481b8(void *, u32, u32);
extern void func_0202a498(u32, void *);
extern u32 func_02072f1c(u32);
extern void func_0204540c(u32, void *, u32, u32);
extern void func_02048308(void);

u16 native_ov003_021d8348(Cell *cell, u32 id, u32 slot, u32 mode, u32 special) {
    char archive[32];
    char filename[32];
    u8 *second;
    u32 count;
    u16 total;
    u32 offset;
    u8 *resource;
    u8 palette;
    s8 index;
    switch (id) {
        case 0x9996:
        case 0x9999:
            count = 0;
            break;
        case 0x9997:
            count = 1;
            break;
        case 0x9995:
        case 0x9998:
            count = 2;
            break;
        default:
            count = func_02044cdc(id);
            if (func_02072f48(id) && special == 0) {
                return func_02061de4(cell, 0x9995, slot, mode, 0);
            }
            break;
    }
    if (mode == 0) {
        count = 0;
    }
    func_0201d444(archive, data_ov003_021e0290);
    total = count + 1;
    for (index = 0; index < total; index++) {
        palette = slot + 1 + index;
        if (palette >= 9) {
            palette = palette + 1;
        }
        func_0201d444(filename, data_ov003_021e02a4, id);
        resource = func_0203cf20(archive, filename, 2);
        if (resource == 0) {
            switch (total - 1) {
                case 0:
                    return func_02061de4(cell, 0x9996, slot, mode, 0);
                case 1:
                    return func_02061de4(cell, 0x9997, slot, mode, 0);
                case 2:
                    return func_02061de4(cell, 0x9998, slot, mode, 0);
            }
        } else {
            func_020481b8(resource, palette * 32, 32);
            func_0202a498(2, resource);
        }
    }
    for (index = 0; index < total; index++) {
        func_0201d444(filename, data_ov003_021e02b4, id);
        second = func_0203cf20(archive, filename, 2);
        if (second) {
            if (mode == 1) {
                offset = 48 + index * 800;
            } else {
                offset = 48 + func_02072f1c(id) * 800;
            }
            func_0204540c(cell->layer, second + offset, cell->first, cell->second);
            func_0202a498(2, second);
        }
        cell++;
    }
    func_02048308();
    return total - 1;
}
