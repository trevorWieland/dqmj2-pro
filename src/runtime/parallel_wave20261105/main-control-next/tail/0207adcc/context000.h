typedef unsigned char u8;

typedef struct {u8 unknown,code,pad[2];} Item;

typedef struct {u8 levels[10];Item items[10];u8 results[10];} Info;

const Info *native_fn_0207aa98(int);
