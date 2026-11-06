#ifndef SCR_NUMERIC_20261029
#define SCR_NUMERIC_20261029
typedef enum { false = 0, true = 1 } bool;
float get_context_value(int index);
float get_numeric_state(int index);
void set_numeric_state(int index, int value);
bool get_primary_flag(int index);
void set_primary_flag(int index, bool enabled);
#endif
