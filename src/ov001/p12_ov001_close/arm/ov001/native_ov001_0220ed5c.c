/* ov001 row 0x0220ed5c: 176 bytes.
 *
 * What it does: 44 instructions; 9 call(s) to 0x0220ecd8, 0x0207b674, 0x0220edb8, +6 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 9 calls (44 instructions, 9 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x5c
 *   branch +0x3c -> +0x5c
 *   branch +0x70 -> +0xa8
 *   branch +0x88 -> +0xa8
 *   test +0x20 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220ed5c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0220ecd8(void);
extern void native_fn_0207b674(void);
extern void native_fn_02210ad0(void);
extern void native_fn_021dbf98(void);


asm u32 native_ov001_0220ed5c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    bl native_fn_0220ecd8
    ldr r1, [r5, #0x1e8]
    orr r4, r0, #0
    add r1, r1, #70
    mov r0, #55
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220ed5c_L5c
    mov r0, r5
    mov r1, #2
    mov r2, #1
    bl native_fn_02210ad0
    cmp r0, #0
    bne ov001_0220ed5c_L5c
    mov r3, #0
    mov r0, r5
    mov r1, #10
    mov r2, #1
    str r3, [sp]
    bl native_fn_021dbf98
    mov r4, #1
ov001_0220ed5c_L5c:
    ldr r1, [r5, #0x1e8]
    mov r0, #56
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0220ed5c_La8
    mov r0, r5
    mov r1, #2
    mov r2, #1
    bl native_fn_02210ad0
    cmp r0, #0
    bne ov001_0220ed5c_La8
    mov r3, #0
    mov r0, r5
    mov r1, #11
    mov r2, #1
    str r3, [sp]
    bl native_fn_021dbf98
    mov r4, #1
ov001_0220ed5c_La8:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
