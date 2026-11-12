/* ov006 row 0x021db5b4: 132 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020677c8(void);
extern void native_fn_02067818(void);
extern void native_fn_021e2f44(void);
extern void native_fn_020677f0(void);


asm u32 native_ov006_021db5b4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x74]
    ldr r2, [r0, #0xc]
    cmp r2, #11
    addls pc, pc, r2, lsl #2
    b L_021db62c
    dcd 0xea00000a
    dcd 0xea00000c
    dcd 0xea00000d
    dcd 0xea00000f
    dcd 0xea00000e
    dcd 0xea00000d
    dcd 0xea00000c
    dcd 0xea00000b
    dcd 0xea00000a
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea000007
    ldr r0, [r0, #0x18]
    bl native_fn_020677c8
    ldmia sp!, {r3, pc}
    bl native_fn_02067818
    ldmia sp!, {r3, pc}
    ldr r0, [r0, #0x18]
    bl native_fn_021e2f44
    ldmia sp!, {r3, pc}
    ldr r1, [r0, #0x18]
    sub r0, r2, #3
    bl native_fn_020677f0
    ldmia sp!, {r3, pc}
L_021db62c:
    mov r0, #0
    ldmia sp!, {r3, pc}
    dcd 0x0220f3b8
}
