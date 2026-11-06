#include "context.h"
int native_main_0209a83c(const char *src, const unsigned long srclen, char *dst, const unsigned long dstlen)
{
	char *srcread_index, *dstwrite_index;
	char read_buffer[4];
	int required_dstsize, i;
	if(srclen %4 != 0)
		return -1;
	required_dstsize = 0;
	for(i=0; i<srclen; i++) {
		if(src[i] != '*')
			required_dstsize += 6;
	}
	required_dstsize = required_dstsize/8;
	if(dst == NULL)
		return required_dstsize;
	if(dstlen < required_dstsize)
		return -1;
	if(srclen == 0) {
		return 0;
	}
	srcread_index = (char *)src;
	dstwrite_index = (char *)dst;
	while(1) {
		for(i=0; i<4; i++) {
			if(srcread_index[i] >= 'A' && srcread_index[i] <= 'Z')
				read_buffer[i] = (char)(srcread_index[i]-'A');
			else if(srcread_index[i] >= 'a' && srcread_index[i] <= 'z')
				read_buffer[i] = (char)(srcread_index[i]-'a'+26);
			else if(srcread_index[i] >= '0' && srcread_index[i] <= '9')
				read_buffer[i] = (char)(srcread_index[i]-'0'+52);
			else if(srcread_index[i] == '.')
				read_buffer[i] = 62;
			else if(srcread_index[i] == '-')
				read_buffer[i] = 63;
			else
				read_buffer[i] = 0;
		}
		srcread_index += 4;
		*dstwrite_index = (char)((read_buffer[0] << 2) | (read_buffer[1] >> 4));
		dstwrite_index++;
		if(dstwrite_index-dst >= required_dstsize)
			break;
		*dstwrite_index = (char)((read_buffer[1] << 4) | (read_buffer[2] >> 2));
		dstwrite_index++;
		if(dstwrite_index-dst >= required_dstsize)
			break;
		*dstwrite_index = (char)((read_buffer[2] << 6) | read_buffer[3]);
		dstwrite_index++;
		if(dstwrite_index-dst >= required_dstsize)
			break;
	}
	return dstwrite_index-dst;
}
