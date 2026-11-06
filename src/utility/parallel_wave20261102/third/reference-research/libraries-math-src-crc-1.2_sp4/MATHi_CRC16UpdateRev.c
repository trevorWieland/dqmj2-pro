typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef u16 MATHCRC16Context;
typedef struct MATHCRC16Table {
	u16 table[256];
} MATHCRC16Table;
void MATHi_CRC16UpdateRev(const MATHCRC16Table * table, MATHCRC16Context * context, const void * input, u32 length);
void MATHi_CRC16UpdateRev (const MATHCRC16Table *table, MATHCRC16Context *context, const void *input, u32 length)
{
	u32 r;
	u32 i;
	const u16 *t = table->table;
	u8 *data = (u8 *)input;
	r = (u32) * context;
	for (i = 0; i < length; i++) {
		r = (r >> 8) ^ t[(r ^ *data) & 0xff];
		data++;
	}
	*context = (MATHCRC16Context) r;
}
