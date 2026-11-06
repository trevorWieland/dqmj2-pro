#ifndef SCR_RUNTIME_CONFIGURATION_20261030
#define SCR_RUNTIME_CONFIGURATION_20261030
enum { object_category = 6 };
extern float dispatch_argument0;
extern float dispatch_argument1;
extern float dispatch_argument2;
extern float dispatch_argument3;
extern float dispatch_argument4;
extern float shared_parameter_first;
extern float shared_parameter_second;
extern float shared_parameter_third;
extern float shared_parameter_fourth;
extern float configured_primary_6;
typedef enum { false = 0, true = 1 } bool;
bool get_primary_flag(int index);
void configure_runtime_object(float category, float first, float second, float third, float fourth, float mode, float selector);
#endif
