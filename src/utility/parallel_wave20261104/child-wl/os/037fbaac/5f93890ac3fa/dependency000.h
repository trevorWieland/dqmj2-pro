typedef unsigned long u32;

typedef volatile u32 vu32;

typedef u32 OSIrqMask;

typedef struct {
	void (*func) (void *);
	u32 enable;
	void * arg;
} OSIrqCallbackInfo;

extern OSIrqCallbackInfo native_utility_child_arm7_data_0380594c[(8 + 1) ];

static inline void OS_SetIrqCheckFlag (OSIrqMask intr)
{
	*(vu32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x38) |= (u32)intr;
}

void native_utility_child_arm7_wram_037fbaac(void);

OSIrqCallbackInfo native_utility_child_arm7_data_0380594c[(8 + 1) ] = {
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, }
};
