/* ov000 row 0x0220ef3c: 220 bytes.
 *
 * What it does: 55 instructions and 4 call(s), then a 8-entry dispatch through an inline branch table at 0x0220ef80 (dispatch word at 0x0220ef78)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020c56b4(void);
extern void native_fn_0203d294(void);


asm u32 native_ov000_0220ef3c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r1, #0
    str r1, [sp]
    mov r9, r0
    mov r8, r1
    mov r11, #12
    mov r10, #25
    mov r4, #50
    mov r5, #75
    mov r6, #100
L_0220ef64:
    mov r0, r9
    bl native_fn_020c56b4
    add r0, r0, r8
    ldrb r0, [r0, #0x10]
    cmp r0, #7
    addls pc, pc, r0, lsl #2
    b L_0220efdc
    dcd 0xea000006
    dcd 0xea000007
    dcd 0xea000008
    dcd 0xea000009
    dcd 0xea00000a
    dcd 0xea00000b
    dcd 0xea00000c
    dcd 0xea00000d
    mov r7, r6
    b L_0220efdc
    mov r7, r5
    b L_0220efdc
    mov r7, r4
    b L_0220efdc
    mov r7, r10
    b L_0220efdc
    mov r7, r11
    b L_0220efdc
    mov r7, #6
    b L_0220efdc
    mov r7, #3
    b L_0220efdc
    mov r7, #0
L_0220efdc:
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, r7
    bge L_0220f004
    mov r0, r9
    bl native_fn_020c56b4
    add r0, r0, r8
    ldrb r0, [r0, #0xe]
    str r0, [sp]
    b L_0220f010
L_0220f004:
    add r8, r8, #1
    cmp r8, #2
    blt L_0220ef64
L_0220f010:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
