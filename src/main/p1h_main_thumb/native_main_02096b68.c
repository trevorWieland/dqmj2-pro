#include "context.h"

extern u32 native_data_021d18e4[];

/* Promote the shared state counter from 4 to 5 once. */
void native_main_02096b68(void)
{
    if (native_data_021d18e4[2] == 4)
        native_data_021d18e4[2] = 5;
}
