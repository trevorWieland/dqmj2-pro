typedef unsigned short int u16;

typedef volatile u16 vu16;

extern const u16 (*ctrdgi_fl_maxtime);

void WUpdateCounter(void);

static void WlIntrCntOvf(void) __attribute__((never_inline));
