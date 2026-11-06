typedef unsigned char u8;
typedef unsigned int u32;
typedef struct Slot5c {u32 key;u8 data[0x58];} Slot5c;
typedef struct Slot10 {u32 key;u32 data;u8 reserved8[8];} Slot10;
typedef struct Slot8 {u32 key;u32 data;} Slot8;
typedef struct Words3 {u32 words[3];} Words3;
typedef struct Object70 {u8 reserved[0x70];Words3 field70;} Object70;
extern void native_fn_02008c14(int,void *,u32);
