/* Kind exclusion test.
 *
 * Kinds 4, 10 and 11 are rejected; every other kind is accepted. The image
 * chains three `cmpne` and falls through to `mov r0, #0` for the rejected set,
 * which is a three-case switch; an OR of equalities would range-collapse.
 * Unknowns: which enum the kind values belong to.
 */
typedef unsigned int u32;

u32 native_ov000_022109b8(u32 kind)
{
    switch (kind) {
    case 4:
    case 10:
    case 11:
        return 0;
    }
    return 1;
}
