typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
u8 native_main_02019bd4(const void * data, u32 dataLength);
static inline u32 MATHi_Checksum8Update (const void *input, u32 length)
{
	u32 sum;
	u32 n;
	sum = 0;
	if (((u32)input) & 1) {
		sum += *((u8 *)input)++;
		length--;
	}
	while ((length >> 17) > 0) {
		length -= (1 << 17);
		for (n = (1 << 16); n > 0; n--) {
			sum += *((u16 *)input)++;
		}
		sum = (sum >> 16) + (sum & 0xffff);
		sum = (u16)(sum + (sum >> 16));
	}
	for (n = (length >> 1); n > 0; n--) {
		sum += *((u16 *)input)++;
	}
	if (length & 1) {
		sum += *((u8 *)input);
	}
	sum = (sum >> 16) + (sum & 0xffff);
	sum += (sum >> 16);
	return (u16)sum;
}
u8 native_main_02019bd4 (const void *data, u32 dataLength)
{
	u32 sum;
	sum = MATHi_Checksum8Update(data, dataLength);
	sum = (sum >> 8) + (sum & 0xff);
	sum += (sum >> 8);
	return (u8)(~sum);
}
