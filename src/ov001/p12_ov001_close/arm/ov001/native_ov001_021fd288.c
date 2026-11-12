/* ov001 row 0x021fd288: 168 bytes.
 *
 * What it does: 41 instructions; 11 call(s) to 0x021fc5b4, 0x022023f8, 0x021fc62c, +8 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (41 instructions, 11 calls, 3 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0xa4 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x14 -> +0x1c
 *   branch +0x30 -> +0x48
 *   branch +0x54 -> +0x6c
 *   back edge +0x90 -> +0x7c
 *   back edge +0x9c -> +0x78
 *   test +0x10 cmp r0, #0
 *   test +0x2c cmp r1, #0
 *   test +0x50 cmp r1, #0
 *   test +0x8c cmp r5, #3
 *   test +0x98 cmp r6, #2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd288; the literal pool and
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

extern void native_fn_021fc5b4(void);
extern void native_fn_022023f8(void);
extern void native_fn_021fc62c(void);
extern void native_fn_021fed58(void);
extern void native_fn_021feb50(void);
extern void native_fn_0202a498(void);
extern void native_fn_02204228(void);
extern void native_fn_021fc574(void);


asm u32 native_ov001_021fd288 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_021fc5b4
    mov r0, #32
    bl native_fn_022023f8
    cmp r0, #0
    bne ov001_021fd288_L1c
    bl native_fn_021fc62c
ov001_021fd288_L1c:
    bl native_fn_021fed58
    bl native_fn_021feb50
    ldr r0, =0x02239c10
    ldr r1, [r0, #0x40]
    cmp r1, #0
    beq ov001_021fd288_L48
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x02239c10
    mov r1, #0
    str r1, [r0, #0x40]
ov001_021fd288_L48:
    ldr r0, =0x02239c10
    ldr r1, [r0, #0x38]
    cmp r1, #0
    beq ov001_021fd288_L6c
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x02239c10
    mov r1, #0
    str r1, [r0, #0x38]
ov001_021fd288_L6c:
    bl native_fn_02204228
    mov r6, #0
    mov r4, r6
ov001_021fd288_L78:
    mov r5, r4
ov001_021fd288_L7c:
    mov r0, r6
    mov r1, r5
    bl native_fn_021fc574
    add r5, r5, #1
    cmp r5, #3
    blt ov001_021fd288_L7c
    add r6, r6, #1
    cmp r6, #2
    blt ov001_021fd288_L78
    ldmia sp!, {r4, r5, r6, pc}
}
