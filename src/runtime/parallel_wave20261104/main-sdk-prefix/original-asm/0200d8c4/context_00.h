typedef unsigned short int u16;
typedef unsigned long long int u64;
typedef struct CPContext {
	u64 div_numer;
	u64 div_denom;
	u64 sqrt;
	u16 div_mode;
	u16 sqrt_mode;
} CPContext;
void native_main_0200d8c4(CPContext * context);
