/* ov001 row 0x022272e8: 276 bytes.
 *
 * What it does: 68 instructions; 14 call(s) to 0x02223fe8, 0x02226bdc, 0x02224900, +11 more; loops (back edge at +0x28); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (68 instructions, 14 calls, 2 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0x110 -> native_data_0222e890 (image word 0x0222e890)
 *   branch +0xb0 -> +0xf8
 *   branch +0xd0 -> +0xec
 *   branch +0xdc -> +0xec
 *   back edge +0xf4 -> +0xc8
 *   test +0xac cmp r0, #2
 *   test +0xcc cmp r1, #0
 *   test +0xd8 cmp r1, #0
 *   test +0xe4 cmp r1, #0
 *   test +0xf0 cmp r4, #3
 *   2 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022272e8; the literal pool and
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

extern u8 native_data_0222e890[];
extern void native_fn_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02224900(void);
extern void native_fn_02225bac(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02225854(void);
extern void native_fn_0222463c(void);
extern void native_fn_02223f20(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_022272e8 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #36
    ldr r1, =native_data_0222e890
    add r3, sp, #24
    mov r5, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r4, [r5, #0x4]
    mov r0, r3
    mov r1, r4
    bl native_fn_02223fe8
    add r0, sp, #24
    mov r1, r5
    mov r2, #21
    bl native_fn_02226bdc
    add r0, sp, #24
    mov r1, r4
    bl native_fn_02224900
    add r0, sp, #24
    mov r1, r4
    mov r2, #55
    bl native_fn_02225bac
    add r0, sp, #24
    mov r1, r4
    mov r2, #54
    bl native_fn_02225bac
    add r0, sp, #24
    add r1, sp, #0
    mov r2, #12
    bl native_fn_02008e0c
    add r0, sp, #24
    mov r1, r4
    bl native_fn_02225854
    add r0, sp, #24
    add r1, sp, #12
    mov r2, #12
    bl native_fn_02008e0c
    mov r1, r4
    add r0, sp, #24
    mov r2, #2
    bl native_fn_0222463c
    add r0, sp, #24
    bl native_fn_02223f20
    cmp r0, #2
    blt ov001_022272e8_Lf8
    mov r4, #0
    mov r0, #1
    add r2, sp, #12
    add r3, sp, #0
    add r12, sp, #24
ov001_022272e8_Lc8:
    ldr r1, [r12, r4, lsl #2]
    cmp r1, #0
    bne ov001_022272e8_Lec
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_022272e8_Lec
    ldr r1, [r2, r4, lsl #2]
    cmp r1, #0
    streq r0, [r12, r4, lsl #2]
ov001_022272e8_Lec:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_022272e8_Lc8
ov001_022272e8_Lf8:
    add r0, sp, #24
    bl native_fn_02224050
    add r0, sp, #24
    bl native_fn_02226cb0
    add sp, sp, #36
    ldmia sp!, {r4, r5, pc}
}
