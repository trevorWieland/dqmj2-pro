typedef unsigned short int u16;
typedef unsigned long u32;
typedef struct MATHCRC16Table {
	u16 table[256];
} MATHCRC16Table;
void native_utility_child_arm9_main_02010b5c(MATHCRC16Table * table, u16 poly);
void native_utility_child_arm9_main_02010b5c (MATHCRC16Table *table, u16 poly)
{
	u32 r;
	u32 i, j;
	u16 *t = table->table;
	for (i = 0; i < 256; i++) {
		r = i;
		for (j = 0; j < 8; j++) {
			if (r & 1) {
				r = (r >> 1) ^ poly;
			} else {
				r >>= 1;
			}
		}
		t[i] = (u16)r;
	}
}
