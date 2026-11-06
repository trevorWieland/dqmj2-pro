typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;

typedef struct { u32 flags; void *record; } Lease;
typedef struct { s16 x; s16 y; } Position;
typedef struct {
    u8 handle;
    u8 padding[3];
    void *record;
    Lease *lease;
    void *first_buffer;
    void *second_buffer;
} State;
typedef struct { u8 padding[0xC84]; u32 flag; } MainState;

extern State data_ov000_02236a84;
extern MainState data_02101ae8;
extern const char data_ov000_0222ee30[];
extern u8 func_02048404(u32, const char *, u32, u32);
extern Lease *func_0204854c(u32, u32);
extern void func_020485b4(Lease *);
extern void func_020484dc(u32, u32);
extern void *func_0202a474(u32, u32);
extern void func_0204b1a0(void *);
extern void func_0204b4f4(void *, const Position *, u32, u32, u32, u32);
extern void func_0204b61c(void *, u32);
extern void func_0204b85c(void *, const Position *, u32, u32, u32, u32, u32);
extern void func_0205fa4c(void *, u32);
extern void func_02048308(void);

u32 native_ov000_021eba48(void) {
    Position position;
    void *buffer;
    u8 handle = func_02048404(1, data_ov000_0222ee30, 4, 2);
    data_ov000_02236a84.handle = handle;
    if (handle != 255) {
        data_ov000_02236a84.lease = func_0204854c(1, handle);
        if (data_ov000_02236a84.lease) {
            data_ov000_02236a84.record = data_ov000_02236a84.lease->record;
            if (data_ov000_02236a84.record) {
                func_0204b1a0(data_ov000_02236a84.record);
                buffer = func_0202a474(72, 4);
                position.x = 0;
                data_ov000_02236a84.second_buffer = buffer;
                position.y = 0;
                func_0204b4f4(data_ov000_02236a84.second_buffer, &position, 32, 2, 2, 36);
                func_0204b61c(data_ov000_02236a84.second_buffer, 0);
                data_ov000_02236a84.first_buffer = func_0202a474(72, 4);
                func_0204b85c(data_ov000_02236a84.first_buffer, &position, 8, 1, 0, 52, 0);
                func_0205fa4c(data_ov000_02236a84.first_buffer, 1);
                data_02101ae8.flag = 1;
                func_02048308();
                return 1;
            }
            func_020485b4(data_ov000_02236a84.lease);
        }
        func_020484dc(1, data_ov000_02236a84.handle);
    }
    return 0;
}
