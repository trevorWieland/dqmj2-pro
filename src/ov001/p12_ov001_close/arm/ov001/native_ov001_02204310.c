/* ov001 row 0x02204310: 224 bytes.
 *
 * What it does: 56 instructions; 10 call(s) to 0x0205f998, 0x0205f8a0, 0x0205f98c, +7 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 10 calls (56 instructions, 10 calls, 3 branches, 10 back edges, 0 literal slots).
 *
 *   branch +0x70 -> +0x90
 *   branch +0x8c -> +0xa8
 *   back edge +0xd4 -> +0x5c
 *   test +0x6c cmp r4, #0
 *   test +0xd0 cmp r4, #2
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204310; the literal pool and
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

extern void native_fn_0205f998(void);
extern void native_fn_0205f8a0(void);
extern void native_fn_0205f98c(void);
extern void native_fn_022023a8(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov001_02204310 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r9, r1
    mov r8, r2
    mov r7, r3
    bl native_fn_0205f998
    mov r2, #2
    mov r0, r10
    mov r1, #1
    strb r2, [r10, #0x22]
    bl native_fn_0205f8a0
    mov r10, r0
    mov r4, #0
    strh r4, [r10, #20]
    strh r4, [r10, #22]
    mov r0, #5
    strb r0, [r10, #0x20]
    mov r0, #1
    strb r0, [r10, #0x21]
    mov r0, #4
    ldrb r6, [sp, #0x28]
    str r0, [r10]
    mov r11, #115
ov001_02204310_L5c:
    ldr r0, [r10, #0x1c]
    and r1, r4, #255
    bl native_fn_0205f98c
    mov r5, r0
    cmp r4, #0
    bne ov001_02204310_L90
    mov r1, r11
    bl native_fn_022023a8
    mov r0, r5
    mov r1, r9
    mov r2, r8
    bl native_fn_02048a60
    b ov001_02204310_La8
ov001_02204310_L90:
    mov r1, #116
    bl native_fn_022023a8
    mov r0, r5
    mov r1, r7
    mov r2, r6
    bl native_fn_02048a60
ov001_02204310_La8:
    ldrb r1, [r10, #0x20]
    mov r0, r5
    bl native_fn_02048a94
    ldrb r1, [r10, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    ldr r0, [r5, #0x7c]
    add r4, r4, #1
    bic r0, r0, #2
    str r0, [r5, #0x7c]
    cmp r4, #2
    blt ov001_02204310_L5c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
