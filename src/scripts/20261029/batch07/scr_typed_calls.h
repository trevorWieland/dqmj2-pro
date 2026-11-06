#ifndef SCR_TYPED_CALLS_20261029
#define SCR_TYPED_CALLS_20261029
typedef enum { false = 0, true = 1 } bool;
float get_context_value(int index);
float get_numeric_state(int index);
void set_numeric_state(int index, int value);
bool get_primary_flag(int index);
void set_primary_flag(int index, bool enabled);
float get_engine_state_code(void);
void select_native_request(float identifier);
void replace_native_request_scalar(float value);
void submit_native_request(float identifier, float x, float y, float z, float value);
void advance_numeric_nine_when_values_match(void);
void process_imported_context(float value);
#endif
