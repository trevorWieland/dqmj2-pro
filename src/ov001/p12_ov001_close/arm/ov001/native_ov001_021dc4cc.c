/* ov001 row 0x021dc4cc: 112 bytes.
 *
 * What it does: 28 instructions; 6 call(s) to 0x021dc230, 0x021db410, 0x021d96d4, +3 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 6 calls (28 instructions, 6 calls, 0 branches, 3 back edges, 0 literal slots).
 *
 *   test +0x14 cmp r3, #0
 *   test +0x1c cmpne r1, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc4cc; the literal pool and
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

extern void native_fn_021dc230(void);
extern void native_fn_021db410(void);
extern void native_fn_021d96d4(void);
extern void native_fn_0220261c(void);
extern void native_fn_0220ecd8(void);
extern void native_fn_021e273c(void);


asm u32 native_ov001_021dc4cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldrb r3, [r6, #0x31c]
    mov r5, r1
    mov r4, r2
    cmp r3, #0
    ldrneb r1, [r6, #0x1ff]
    cmpne r1, #0
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
    mov r1, #0
    bl native_fn_021dc230
    mov r0, r6
    and r1, r5, #255
    bl native_fn_021db410
    mov r0, r6
    and r1, r4, #255
    bl native_fn_021d96d4
    ldrb r0, [r6, #0x31e]
    ldrb r1, [r6, #0x31f]
    mov r2, #1
    bl native_fn_0220261c
    mov r0, r6
    bl native_fn_0220ecd8
    mov r0, r6
    bl native_fn_021e273c
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
