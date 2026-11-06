typedef unsigned int size_t;
typedef char *va_list;
typedef unsigned long u32;
typedef unsigned long long int u64;
extern int native_main_0201a670(char * dst, size_t len, const char * fmt, va_list vlist);
typedef struct dst_string_tag {
    size_t len;
    char * cur;
    char * base;
} dst_string;
void native_fn_0201a594 (dst_string * p, char c);
void native_fn_0201a5c4 (dst_string * p, char c, int n);
void native_fn_0201a618 (dst_string * p, const char * s, int n);
