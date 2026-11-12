/* ov000 row 0x021e3f98: 124 bytes.
 *
 * What it does: 30 instructions; 6 call(s) to 0x0201d444, 0x0201d984, 0x0201f274, +3 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x78 -> native_data_0222eca4 (image word 0x0222eca4)
 *   branch +0x30 -> +0x44
 *   branch +0x50 -> +0x6c
 *   test +0x28 cmp r0, #0
 *   test +0x4c cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e3f98; the literal pool and
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

extern void native_fn_0201d444(void);
extern u8 native_data_0222eca4[];
extern void native_fn_0201d984(void);
extern void native_fn_0201f274(void);
extern void native_fn_021dfa5c(void);
extern void native_fn_02211188(void);


asm u32 native_ov000_021e3f98 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #32
    mov r6, r0
    add r0, sp, #0
    mov r1, r6
    mov r5, #0
    bl native_fn_0201d444
    ldr r1, =native_data_0222eca4
    add r0, sp, #2
    bl native_fn_0201d984
    cmp r0, #0
    moveq r4, r5
    beq ov000_021e3f98_L44
    mov r1, r5
    strb r1, [r0], #1
    bl native_fn_0201f274
    mov r4, r0
ov000_021e3f98_L44:
    add r0, sp, #0
    bl native_fn_021dfa5c
    cmp r0, #0
    ble ov000_021e3f98_L6c
    mov r3, r4
    add r1, r6, #32
    add r2, r6, #44
    bl native_fn_02211188
    cmp r0, #0
    movne r5, #1
ov000_021e3f98_L6c:
    mov r0, r5
    add sp, sp, #32
    ldmia sp!, {r4, r5, r6, pc}
}
