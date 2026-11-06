typedef unsigned int u32;
typedef unsigned short u16;
typedef void (*IrqCallback)(void *);
typedef struct CallbackRecord {
    IrqCallback function;
    u32 enabled;
    void *argument;
} CallbackRecord;
typedef char CallbackRecord_Size12[(sizeof(CallbackRecord)==12)?1:-1];
extern CallbackRecord native_utility_child_arm7_callbacks_0380594c[];
extern const u16 native_utility_child_arm7_irq_indices_0380581c[];
extern u32 native_utility_child_arm7_arm_037fbc50(u32);
extern void native_utility_child_arm7_arm_037fbb84(u32);
#define NATIVE_IRQ_CHECK_WORD (*(volatile u32 *)0x0380FFF8)
