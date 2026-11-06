typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u32 flags;
    void *record;
} Resource;

typedef struct {
    u8 first_handle;
    u8 second_handle;
    u8 reserved[2];
    void *first_buffer;
    void *second_buffer;
    void *second_tiles;
    void *second_payload;
    Resource *second_resource;
    void *second_map;
    void *first_map;
    void *first_payload;
    Resource *first_resource;
    void *second_auxiliary;
} Manager;

typedef struct { u8 reserved[0x540]; u32 notification; } MainFlags;
typedef struct { u8 reserved[0xC84]; u32 notification; } SubFlags;

extern Manager data_ov007_021da9dc;
extern MainFlags data_020feae8;
extern SubFlags data_02101ae8;
extern const char data_ov007_021da8e8[];
extern const char data_ov007_021da8fc[];
extern void func_02048308(void);
extern u8 func_02048404(u32, const char *, u32, u32);
extern Resource *func_0204854c(u32, u32);
extern void *func_0202a474(u32, u32);
extern void func_020485b4(Resource *);
extern void func_020484dc(u32, u32);
extern void func_ov007_021d89c0(void);
extern void func_ov007_021d8db8(void);
extern void func_ov007_021d8e4c(void);
extern void func_ov007_021d8ee8(void);
extern void func_ov007_021d8fbc(u32);

u32 native_ov007_021d8af8(void) {
    u8 handle = func_02048404(0, data_ov007_021da8e8, 4, 5);
    data_ov007_021da9dc.first_handle = handle;
    if (handle != 255) {
        data_ov007_021da9dc.first_resource = func_0204854c(0, handle);
        if (data_ov007_021da9dc.first_resource) {
            data_ov007_021da9dc.first_payload = data_ov007_021da9dc.first_resource->record;
            if (data_ov007_021da9dc.first_payload) {
                data_ov007_021da9dc.first_map = func_0202a474(144, 4);
                func_ov007_021d89c0();
                data_ov007_021da9dc.first_buffer = func_0202a474(144, 4);
                func_ov007_021d8fbc(0);
                data_020feae8.notification = 1;
                func_02048308();
                return 1;
            }
            func_020485b4(data_ov007_021da9dc.first_resource);
        }
        func_020484dc(0, data_ov007_021da9dc.first_handle);
    }
    return 0;
}

u32 native_ov007_021d9040(void) {
    u8 handle = func_02048404(1, data_ov007_021da8fc, 4, 5);
    data_ov007_021da9dc.second_handle = handle;
    if (handle != 255) {
        data_ov007_021da9dc.second_resource = func_0204854c(1, handle);
        if (data_ov007_021da9dc.second_resource) {
            data_ov007_021da9dc.second_payload = data_ov007_021da9dc.second_resource->record;
            if (data_ov007_021da9dc.second_payload) {
                data_ov007_021da9dc.second_tiles = func_0202a474(2304, 4);
                func_ov007_021d8db8();
                data_ov007_021da9dc.second_buffer = func_0202a474(144, 4);
                func_ov007_021d8e4c();
                data_ov007_021da9dc.second_map = func_0202a474(432, 4);
                func_ov007_021d8ee8();
                data_ov007_021da9dc.second_auxiliary = func_0202a474(144, 4);
                func_ov007_021d8fbc(1);
                data_02101ae8.notification = 1;
                func_02048308();
                return 1;
            }
            func_020485b4(data_ov007_021da9dc.second_resource);
        }
        func_020484dc(1, data_ov007_021da9dc.second_handle);
    }
    return 0;
}
