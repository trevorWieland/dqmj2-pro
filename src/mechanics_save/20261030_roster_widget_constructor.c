typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Widget {
    u8 prefix[4];
    u8 index;
    u8 pad[3];
    u8 animation[0x74];
    u32 flags;
    u8 copied;
} Widget;
typedef struct Descriptor {
    u8 prefix[0x10];
    void *sequenceBank;
    void *cellBank;
    u8 pad[0x49];
    u8 copied;
} Descriptor;
extern u32 native_fn_020346a8(void *bank, u32 index);
extern u32 native_fn_02035108(void *animation, u32 sequence, s32 cellBankWord);
extern void native_fn_02035000(void *animation, s32 mode, s32 userWord, s32 callbackWord);
extern void native_fn_02048a5c(void);
u32 native_main_02048644(Widget *widget, const Descriptor *descriptor, u32 index) {
    widget->copied = descriptor->copied;
    widget->index = index;
    native_fn_02035108(widget->animation, native_fn_020346a8(descriptor->sequenceBank, index), (s32)descriptor->cellBank);
    native_fn_02035000(widget->animation, 1, (s32)&widget, (s32)native_fn_02048a5c);
    widget->flags |= 2;
    return 0;
}
