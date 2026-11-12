/* ov000 row 0x021f8990: 284 bytes.
 *
 * What it does: 68 instructions; 15 call(s) to 0x0201d444, 0x0205ff80, 0x020602dc, +12 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x110 -> native_data_0222f3d8 (image word 0x0222f3d8)
 *   pool +0x114 -> native_data_0222b9cc (image word 0x0222b9cc)
 *   pool +0x118 -> native_data_0222f3ec (image word 0x0222f3ec)
 *   back edge +0x30 -> +0x18
 *   back edge +0xa4 -> +0x6c
 *   test +0xa0 cmp r8, #25
 *   test +0xe8 tst r1, #3
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f8990; the literal pool and
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

extern u8 native_data_0222f3d8[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern void native_fn_020602dc(void);
extern void native_fn_0204b078(void);
extern u8 native_data_0222b9cc[];
extern void native_fn_02007308(void);
extern void native_fn_02004b00(void);
extern void native_fn_0205ff9c(void);
extern u8 native_data_0222f3ec[];
extern void native_fn_020482b4(void);
extern void native_fn_02048308(void);


asm u32 native_ov000_021f8990 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #32
    mov r10, r0
    add r2, sp, #0
    mov r1, #8
    mov r0, #0
ov000_021f8990_L18:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_021f8990_L18
    ldr r1, =native_data_0222f3d8
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0205ff80
    bl native_fn_020602dc
    mov r2, r10
    mov r1, #0
    bl native_fn_0204b078
    mov r6, #32
    ldr r5, =native_data_0222b9cc
    mov r9, r0
    mov r8, #0
    mov r4, r6
ov000_021f8990_L6c:
    mov r0, r8, lsl #5
    add r7, r0, #4
    mov r1, r6
    add r0, r9, r7
    bl native_fn_02007308
    ldrb r1, [r5, r8]
    mov r2, r4
    add r0, r9, r7
    mov r1, r1, lsl #5
    add r1, r1, #2432
    bl native_fn_02004b00
    add r0, r8, #1
    and r8, r0, #255
    cmp r8, #25
    blo ov000_021f8990_L6c
    bl native_fn_0205ff9c
    ldr r1, =native_data_0222f3ec
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0205ff80
    bl native_fn_020602dc
    mov r2, r10
    mov r1, #2
    bl native_fn_0204b078
    ldrb r2, [r0]
    ldrb r1, [r0, #0x1]
    add r0, r0, #2
    smulbb r1, r2, r1
    mov r1, r1, lsl #1
    add r1, r1, #2
    tst r1, #3
    addne r0, r0, #2
    mov r1, #96
    mov r2, #32
    bl native_fn_020482b4
    bl native_fn_0205ff9c
    bl native_fn_02048308
    mov r0, #1
    add sp, sp, #32
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
