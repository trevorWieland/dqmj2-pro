#include "context.h"
Vec3 *native_main_020285c8(Node *node, Vec3 *output)
{
    if (!node) node = native_data_020edd0c.current;
    if (output) *output = node->target;
    return &node->target;
}
