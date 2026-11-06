extern const unsigned short native_data_020d8e04[128];

extern const unsigned char native_data_020d8d84[128];

static inline int isspace(int c) {if(c<0 || c>=128)return 0;return native_data_020d8e04[c]&0x100;}

static inline int isdigit(int c) {if(c<0 || c>=128)return 0;return native_data_020d8e04[c]&8;}

static inline int isalpha(int c) {if(c<0 || c>=128)return 0;return native_data_020d8e04[c]&1;}

static inline int toupper(int c) {if(c<0 || c>=128)return c;return native_data_020d8d84[c];}

enum scan_states
{
    start           = 0x01,
    check_for_zero  = 0x02,
    leading_zero    = 0x04,
    need_digit      = 0x08,
    digit_loop      = 0x10,
    finished        = 0x20,
    failure         = 0x40
};
