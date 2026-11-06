typedef struct decimal {char sign;char pad1;short exp;struct {unsigned char length;unsigned char text[32];unsigned char pad37;} sig;} decimal;

void native_main_02020120(decimal *dec, int new_length);
