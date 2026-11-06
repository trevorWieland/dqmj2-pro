#include "context.h"
int native_main_0209a738(const char *src, const unsigned long srclen, char *dst, const unsigned long dstlen)
{
	int required_dstsize, num_dstout, num_srcin;
	char *srcread_index, *tail_src, *dstwrite_index;
	unsigned char read_buffer[3];
	required_dstsize = (int)((srclen/3*4)+(srclen%3 != 0 ? 4 : 0));
	if(dst == NULL)
		return required_dstsize;
	if(dstlen < required_dstsize)
		return -1;
	srcread_index =	 (char *)src;
	tail_src = (char *)src+srclen;
	dstwrite_index = (char *)dst;
	while(srcread_index != tail_src) {
		num_dstout = (tail_src-srcread_index);
		num_dstout = num_dstout*8/6+(num_dstout*8%6 != 0 ? 1 : 0);
		num_srcin = tail_src-srcread_index < 3 ? tail_src-srcread_index : 3;
		native_fn_02008d78(read_buffer, 0x00, 3);
		native_fn_02008e0c(srcread_index, read_buffer, (unsigned long)num_srcin);
		*dstwrite_index = native_data_020df358[read_buffer[0] >> 2];
		dstwrite_index++;
		if(num_dstout >= 2)
			*dstwrite_index = native_data_020df358[(read_buffer[0] << 4) & 0x3f | (read_buffer[1] >> 4)];
		else
			*dstwrite_index = '*';
		dstwrite_index++;
		if(num_dstout >= 3)
			*dstwrite_index = native_data_020df358[(read_buffer[1] << 2) & 0x3f | (read_buffer[2] >> 6)];
		else
			*dstwrite_index = '*';
		dstwrite_index++;
		if(num_dstout >= 4)
			*dstwrite_index = native_data_020df358[read_buffer[2] & 0x3f];
		else
			*dstwrite_index = '*';
		dstwrite_index++;
		srcread_index += num_srcin;
	}
	return dstwrite_index-dst;
}
