typedef unsigned char u8;
typedef unsigned int u32;
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
extern u32 func_0201d69c(const char *);
extern void func_02008d78(void *, u32, u32);
extern void func_02048e14(Record *);
extern void func_02008c14(u32, void *, u32);

void native_main_020484dc(u32 bank, u32 record_index) {
    Record *record = (Record *)((u32)data_020fbae8 + bank * 0x3744 + record_index * 100);
    if ((record->flags & 1) == 1) {
        u32 length = func_0201d69c(record->name);
        func_02008d78(record->name, 0, length);
        func_02048e14(record);
        record->flags &= ~1;
        func_02008c14(0, record, 100);
    }
}
