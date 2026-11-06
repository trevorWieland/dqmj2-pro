typedef unsigned int u32;typedef struct{u32 s_addr;}IN_ADDR;
#define ntohl(x) (((x)>>24&0xff)|((x)>>8&0xff00)|((x)<<8&0xff0000)|((x)<<24&0xff000000))
