typedef unsigned int u32;
extern unsigned char native_data_021e7298[];
extern unsigned char native_data_021e9894[];
typedef struct Pair {
    signed char first;
    unsigned char second;
} Pair;
extern Pair native_data_021e6e84[];
extern void native_fn_0201d444(void *, const void *);
extern void native_fn_0205ff80(void *);
extern int native_fn_02065730(void *, int, int, int, int);
extern void native_fn_0205ff9c(void);
extern void native_fn_02045dc4(int, int, int, int, int, int);
void native_ov005_021dbb80(void)
{
    unsigned char context[32];
    int position = 128;
    unsigned char *output;
    signed char index;
    native_fn_0201d444(context, native_data_021e7298);
    native_fn_0205ff80(context);
    output = native_data_021e9894;
    index = 0;
    do {
        position += native_fn_02065730(output, native_data_021e6e84[index].first, 0,
                                      native_data_021e6e84[index].second, position);
        output += 12;
        index++;
    } while (index < 3);
    native_fn_0205ff9c();
    native_fn_02045dc4(0, 2, 0, 0, 32, 32);
}
