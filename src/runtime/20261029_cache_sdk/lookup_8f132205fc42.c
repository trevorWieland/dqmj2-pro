typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Candidate;
typedef struct {
    u32 field0;
    u32 field4;
    u8 reserved08[16];
    char name[64];
    u32 field58;
    u32 flags;
    u32 field60;
} Record;

extern u8 data_020fbae8[];
extern int func_0201d800(const char *, const char *);
extern u32 func_0201d69c(const char *);
extern Record *func_02048aa4(Record *, u32, u32, const char *, u32, u32);
extern void func_02008d78(void *, u32, u32);
extern void func_02048e14(Record *);
extern void func_02008c14(u32, void *, u32);

u8 native_main_02048404(u32 bank, const char *name, u32 argument2, u32 argument3) {
    u8 index;
    u32 offset = bank * 0x3744;
    Record *records = (Record *)(offset + (u32)data_020fbae8);
    index = 0;
    do {
        if (func_0201d800(records[index].name, name) == 0) {
            return index;
        }
        index++;
    } while (index < 8);
    index = 0;
    do {
        if ((records[index].flags & 1) != 1) {
            Record *loaded;
            func_0201d69c(name);
            loaded = func_02048aa4(records, bank, index, name, argument2, argument3);
            loaded->flags |= 1;
            return index;
        }
        index++;
    } while (index < 8);
    return 255;
}

