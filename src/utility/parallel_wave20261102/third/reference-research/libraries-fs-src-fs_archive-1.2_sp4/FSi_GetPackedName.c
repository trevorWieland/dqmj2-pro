typedef unsigned char u8;
typedef unsigned long u32;
    static inline u8 MI_ReadByte (const void * address)
    {
        return *(u8 *)address;
    }
enum {
	FS_ARCHIVE_NAME_LEN_MAX = 3
};
static u32 FSi_GetPackedName (const char *name, int name_len)
{
	u32 ret = 0;
	if (name_len <= FS_ARCHIVE_NAME_LEN_MAX) {
		int i = 0;
		for (; i < name_len; ++i) {
			u32 c = (u32)MI_ReadByte(name + i);
			if (!c)
				break;
			c = (u32)(c - 'A');
			if (c <= (u32)('Z' - 'A'))
				c = (u32)(c + 'a');
			else
				c = (u32)(c + 'A');
			ret |= (u32)(c << (i * 8));
		}
	}
	return ret;
}
