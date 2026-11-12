/* ov001 row 0x0220815c: 180 bytes.
 *
 * What it does: 45 instructions; 9 call(s) to 0x02207938, 0x0205f998, 0x02208170, +6 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 9 calls (45 instructions, 9 calls, 0 branches, 9 back edges, 0 literal slots).
 *
 *   back edge +0x28 -> +0x14
 *   test +0x20 cmp r5, #16
 *   test +0x34 cmp r0, #1
 *   test +0x90 cmp r0, #0
 *   test +0x98 cmpne r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220815c; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_0205f998(void);
extern void native_fn_0206cf44(void);
extern void native_fn_0206d114(void);
extern void native_fn_02202374(void);
extern void native_fn_02072f1c(void);
extern void native_fn_0206d838(void);
extern void native_fn_021fefb0(void);


asm u32 native_ov001_0220815c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_02207938
    mov r4, r0
    add r6, r4, #184
    mov r5, #0
ov001_0220815c_L14:
    mov r0, r6
    bl native_fn_0205f998
    add r5, r5, #1
    cmp r5, #16
    add r6, r6, #72
    blt ov001_0220815c_L14
    ldr r0, [r4, #0x24]
    ldr r5, [r4, #0x538]
    cmp r0, #1
    ldrsb r0, [r5, #12]
    moveq r7, #127
    mov r1, #16
    mov r2, #12
    movne r7, #6
    ldr r6, [r4, #0x10]
    bl native_fn_0206cf44
    ldrsb r0, [r5, #12]
    mov r1, #1
    bl native_fn_0206d114
    bl native_fn_02202374
    mov r4, r0
    ldr r0, [r6, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02072f1c
    mov r2, r0
    ldrsb r1, [r5, #12]
    and r3, r7, #255
    mov r0, r4
    bl native_fn_0206d838
    ldrb r0, [r6, #0x31c]
    ldrsb r1, [r5, #12]
    cmp r0, #0
    ldrneb r0, [r6, #0x1ff]
    cmpne r0, #0
    add r0, r6, #768
    movne r2, #1
    ldrsb r0, [r0, #30]
    moveq r2, #0
    bl native_fn_021fefb0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
