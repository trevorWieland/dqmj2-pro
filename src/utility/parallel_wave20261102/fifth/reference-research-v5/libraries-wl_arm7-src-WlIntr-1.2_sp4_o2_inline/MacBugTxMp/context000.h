typedef unsigned short int u16;

typedef unsigned long u32;

typedef volatile u16 vu16;

typedef u32 OSIrqMask;

OSIrqMask OS_EnableIrqMask(OSIrqMask intr);

OSIrqMask OS_DisableIrqMask(OSIrqMask intr);

extern const u16 (*ctrdgi_fl_maxtime);

static void WlIntrMpEnd(u32 bMacBugPatch);

void MacBugTxMp(void *arg);

void WlIntrMpEnd(u32 bMacBugPatch);
