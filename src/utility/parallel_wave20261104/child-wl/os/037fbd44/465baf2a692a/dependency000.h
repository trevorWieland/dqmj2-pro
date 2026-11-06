typedef unsigned long u32;

typedef u32 OSIrqMask;

typedef void (*OSIrqFunction) (void);

typedef struct {
	void (*func) (void *);
	u32 enable;
	void * arg;
} OSIrqCallbackInfo;

extern OSIrqFunction native_utility_child_arm7_data_03805830[];

extern OSIrqCallbackInfo native_utility_child_arm7_data_0380594c[(8 + 1) ];

void native_utility_child_arm7_wram_037fbd44(OSIrqMask intrBit, OSIrqFunction function);
