typedef unsigned int size_t;
typedef struct dst_string_tag {
    size_t len;
    char * cur;
    char * base;
} dst_string;
