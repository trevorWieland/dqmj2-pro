/* ov001 row 0x021d9124: 240 bytes.
 *
 * What it does: 58 instructions; 9 call(s) to 0x0202a37c, 0x0200bd04, 0x0200bfe4, +6 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (58 instructions, 9 calls, 2 branches, 8 back edges, 2 literal slots).
 *
 *   pool +0xe8 -> constant 0x02232b20 (image word 0x02232b20)
 *   pool +0xec -> native_data_0222eabc (image word 0x0222eabc)
 *   branch +0x3c -> +0xdc
 *   branch +0x58 -> +0xdc
 *   branch +0x84 -> +0xc0
 *   back edge +0xcc -> +0x7c
 *   test +0x34 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0xc4 cmp r9, #3
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d9124; the literal pool and
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

extern void native_fn_0202a37c(void);
extern void native_fn_0200bd04(void);
extern u8 native_data_0222eabc[];
extern void native_fn_0200bfe4(void);
extern void native_fn_0200c190(void);
extern void native_fn_0200c180(void);
extern void native_fn_02007308(void);
extern void native_fn_0200c02c(void);


asm u32 native_ov001_021d9124 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #84
    ldr r4, =0x02232b20
    str r1, [sp]
    strb r0, [r4]
    ldrsb r0, [r4]
    str r2, [sp, #0x4]
    mov r1, #300
    mov r2, #4
    str r3, [sp, #0x8]
    mov r4, #0
    bl native_fn_0202a37c
    ldr r1, =0x02232b20
    cmp r0, #0
    str r0, [r1, #0x4]
    beq ov001_021d9124_Ldc
    add r0, sp, #12
    bl native_fn_0200bd04
    ldr r1, =native_data_0222eabc
    add r0, sp, #12
    bl native_fn_0200bfe4
    cmp r0, #0
    beq ov001_021d9124_Ldc
    mov r9, r4
    mov r11, #100
    mov r6, r4
    ldr r5, =0x02232b20
    mov r10, r9
    add r7, sp, #12
    add r8, sp, #0
    mov r4, r11
ov001_021d9124_L7c:
    ldr r0, [r8, r9, lsl #2]
    cmp r0, #0
    blt ov001_021d9124_Lc0
    mul r1, r0, r4
    mov r0, r7
    mov r2, r6
    add r1, r1, #8
    bl native_fn_0200c190
    ldr r1, [r5, #0x4]
    mov r0, r7
    add r1, r1, r10
    mov r2, r11
    bl native_fn_0200c180
    ldr r0, [r5, #0x4]
    mov r1, #100
    add r0, r0, r10
    bl native_fn_02007308
ov001_021d9124_Lc0:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #100
    blt ov001_021d9124_L7c
    add r0, sp, #12
    bl native_fn_0200c02c
    mov r4, #1
ov001_021d9124_Ldc:
    mov r0, r4
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
