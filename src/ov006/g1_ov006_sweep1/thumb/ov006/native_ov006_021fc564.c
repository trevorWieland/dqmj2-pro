/* ov006 row 0x021fc564: 112 bytes.
 *
 * What it does (from the measured stream): registers three resource descriptors
 * through the shared helper at 0x021f27d4, then forces the low two bits of
 * five display-control halfwords to 3: two on the sub engine at 0x04001008 and
 * three on the main engine at 0x04000008.  The helper's contract and the five
 * registers' meanings are not established by byte identity.
 *
 * Generated, not hand-written: this is member 2 of a six-row
 * coarse-skeleton family (identical opcode/register/width skeleton, only the
 * literal-pool pointers differ).  The representative 0x021f7a10 matched its C
 * body byte- and relocation-exactly on the first compile; the other five were
 * instantiated from the same template with the pointers read from their own
 * pool.  Rule: src/ov006/g1_ov006_sweep1/thumb/** (p033, mwccarm 2.0/sp1p5).
 *
 * Unknowns: what the three descriptors configure, and which engine consumer
 * reads the five control halfwords.
 */
typedef unsigned short u16;
typedef unsigned int u32;

extern void fn_021f27d4(u32 a, u32 b);

void native_ov006_021fc564(void)
{
    fn_021f27d4(0x0220dfbc, 0x02004fd8);
    fn_021f27d4(0x0220dfd4, 0x020048a0);
    fn_021f27d4(0x0220dfec, 0x02004cd8);
    *(volatile u16 *)0x04001008 = (*(volatile u16 *)0x04001008 & ~3u) | 3u;
    *(volatile u16 *)0x0400100a = (*(volatile u16 *)0x0400100a & ~3u) | 3u;
    *(volatile u16 *)0x04000008 = (*(volatile u16 *)0x04000008 & ~3u) | 3u;
    *(volatile u16 *)0x0400000a = (*(volatile u16 *)0x0400000a & ~3u) | 3u;
    *(volatile u16 *)0x0400000c = (*(volatile u16 *)0x0400000c & ~3u) | 3u;
}
