#include "context.h"
Vec3 *native_main_0202859c(Node *node, Vec3 *output)
{
    if (!node) node = native_data_020edd0c.current;
    if (output) *output = node->position;
    return &node->position;
}
