typedef unsigned char u8;
typedef unsigned long u32;
    static inline u8 MI_ReadByte (const void * address)
    {
        return *(u8 *)address;
    }
int FSi_StrNICmp(const char * str1, const char * str2, u32 len);
int FSi_StrNICmp (const char *str1, const char *str2, u32 len)
{
	int i;
	for (i = 0; i < len; ++i) {
		u32 c = (u32)(MI_ReadByte(str1 + i) - 'A');
		u32 d = (u32)(MI_ReadByte(str2 + i) - 'A');
		if (c <= 'Z' - 'A')
			c += 'a' - 'A';
		if (d <= 'Z' - 'A')
			d += 'a' - 'A';
		if (c != d)
			return (int)(c - d);
	}
	return 0;
}
