#ifndef SCR_RESET_CALLER_20261030
#define SCR_RESET_CALLER_20261030
typedef enum { false = 0, true = 1 } bool;
void set_primary_flag(int index, bool enabled);
void set_numeric_state(int index, float value);
void reset_runtime_counter(float blocks);
float sample_signed_random(float bound);
bool runtime_counter_at_threshold(void);
void reset_shared_flags(void);
void advance_world_numeric_state(void);
void refresh_shared_context(void);
void run_world_context_updates(void);
void apply_saved_world_argument(float value);
void before_primary_flag_reset(void);
void finalize_world_state(void);
#endif
