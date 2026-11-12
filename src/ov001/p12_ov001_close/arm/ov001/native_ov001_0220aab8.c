/* ov001 row 0x0220aab8: 232 bytes.
 *
 * What it does: 54 instructions; 12 call(s) to 0x0202a250, 0x0201d444, 0x0205ff80, +9 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (54 instructions, 12 calls, 0 branches, 12 back edges, 4 literal slots).
 *
 *   pool +0xd8 -> native_data_0222f130 (image word 0x0222f130)
 *   pool +0xdc -> native_data_0222f0f0 (image word 0x0222f0f0)
 *   pool +0xe0 -> constant 0x0223df58 (image word 0x0223df58)
 *   pool +0xe4 -> native_data_0222f144 (image word 0x0222f144)
 *   back edge +0x78 -> +0x3c
 *   test +0x6c cmp r4, #21
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220aab8; the literal pool and
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

extern void native_fn_0202a250(void);
extern u8 native_data_0222f130[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222f0f0[];
extern void native_fn_0205ffcc(void);
extern void native_fn_0205ff9c(void);
extern u8 native_data_0222f144[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);


asm u32 native_ov001_0220aab8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #48
    mov r1, #0
    mov r9, r0
    strh r1, [sp, #4]
    bl native_fn_0202a250
    mov r5, r0
    ldr r1, =native_data_0222f130
    add r0, sp, #16
    bl native_fn_0201d444
    add r0, sp, #16
    bl native_fn_0205ff80
    ldr r6, =native_data_0222f0f0
    ldr r7, =0x0223df58
    mov r4, #0
ov001_0220aab8_L3c:
    ldrb r8, [r6, #0x2]
    mov r0, r7
    ldr r1, [r9, r8, lsl #2]
    mov r3, r8
    str r1, [sp]
    ldrsb r1, [r6]
    ldrb r2, [r6, #0x1]
    bl native_fn_0205ffcc
    ldr r1, [r9, r8, lsl #2]
    add r4, r4, #1
    add r0, r1, r0
    str r0, [r9, r8, lsl #2]
    cmp r4, #21
    add r6, r6, #3
    add r7, r7, #12
    blt ov001_0220aab8_L3c
    bl native_fn_0205ff9c
    ldr r0, =native_data_0222f144
    mov r1, r5
    bl native_fn_0203cc2c
    mov r4, r0
    add r0, sp, #8
    mov r1, r4
    mov r2, #0
    bl native_fn_0204518c
    ldr r0, [sp, #0x8]
    ldr r2, [sp, #0xc]
    mov r1, #0
    bl native_fn_0204820c
    add r0, sp, #4
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r0, r5
    mov r1, r4
    bl native_fn_0202a498
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
