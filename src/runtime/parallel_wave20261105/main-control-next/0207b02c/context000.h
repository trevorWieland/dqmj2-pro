typedef unsigned char u8;

typedef unsigned short u16;

typedef struct {u8 pad0[4];u16 flags;u8 pad6[34];} Row40;

typedef struct {unsigned int pad0;Row40 *rows;} State;

extern State native_data_021c6744;
