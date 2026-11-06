#include "context.h"
void native_main_0204b82c(int row, int column, void **table)
{
    int index = row * 3 + column;
    if (table[index]) {
        native_fn_0202a498(2, table[index]);
        table[index] = 0;
    }
}
