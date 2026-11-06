typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 prefix; u16 packed; } NativeDescriptor;
typedef struct { u8 prefix[24]; s16 species; } SavedRecord;
extern SavedRecord *native_fn_02062a10(u32);
extern NativeDescriptor *native_fn_020449d4(int);
u32 native_main_020640b4(u32 id) {
    SavedRecord *record;
    if (id != 0) {
        record = native_fn_02062a10(id);
        if (record) return (u8)(((u32)native_fn_020449d4(record->species)->packed << 24) >> 28);
    }
    return 0;
}
