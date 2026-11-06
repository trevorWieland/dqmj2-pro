typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {u8 pad[0x7C];u32 flags;} Object;
typedef struct {u8 pad[0xC];Object *object;} Context;
typedef struct {u8 pad[0xC84];u32 dirty;} Signal;
extern u8 native_data_ov003_021e041c[];
extern Context native_data_ov003_021e0d18;
extern Signal native_data_02101ae8;
