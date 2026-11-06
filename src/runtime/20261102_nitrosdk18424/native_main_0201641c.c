typedef unsigned short int u16;
typedef unsigned long u32;
extern const u16 (*ctrdgi_fl_maxtime);
u16 native_main_0201641c(const u16 * buf, int length);
u16 native_main_0201641c (const u16 * buf, int length)
{
	u32 sum;
	int nwords = length >> 1;
	for (sum = 0; nwords > 0; nwords--)
		sum += *buf++;
	sum = (sum >> 16) + (sum & 0xffff);
	sum += (sum >> 16);
	return (u16)(sum ^ 0xffff);
}
