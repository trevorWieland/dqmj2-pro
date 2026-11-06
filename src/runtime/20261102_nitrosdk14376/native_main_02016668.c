typedef unsigned short int u16;
extern const u16 (*ctrdgi_fl_maxtime);
int native_main_02016668(u16 * str);
int native_main_02016668 (u16 * str)
{
	int len = 0;
	while (*str++)
		len++;
	return len;
}
