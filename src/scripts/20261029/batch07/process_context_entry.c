#include "scr_typed_calls.h"
void process_context_entry(void)
{
    float context_value = get_context_value(0);
    float engine_state = get_engine_state_code();
    advance_numeric_nine_when_values_match();
    process_imported_context(context_value);
    if (engine_state == 57) {
        if (context_value == 59) {
            bool primary_222 = get_primary_flag(222);
            if (primary_222 == false) {
                set_primary_flag(262, true);
            }
        }
    } else {
        if (context_value == 66) {
            select_native_request(130);
            set_numeric_state(50, 0);
            set_numeric_state(51, 4);
            replace_native_request_scalar(90);
            submit_native_request(130, -38.97f, 0, 0, 90);
        }
    }
}
