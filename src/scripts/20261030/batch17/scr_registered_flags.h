#ifndef SCR_REGISTERED_FLAGS_20261030
#define SCR_REGISTERED_FLAGS_20261030
typedef enum { false = 0, true = 1 } bool;
bool get_primary_flag(int index);
void set_primary_flag(int index, bool enabled);
#endif
