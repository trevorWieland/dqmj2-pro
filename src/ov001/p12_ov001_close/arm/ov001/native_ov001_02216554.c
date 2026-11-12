/* ov001 row 0x02216554: 184 bytes.
 *
 * What it does: 38 instructions; no calls; no back edge; returns through pop {r3, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: branched body (38 instructions, 1 call, 19 branches, 0 back edges, 8 literal slots).
 *
 *   pool +0x98 -> constant 0x02242ba0 (image word 0x02242ba0)
 *   pool +0x9c -> native_fn_022154d8 (image word 0x022154d8)
 *   pool +0xa0 -> native_fn_02215710 (image word 0x02215710)
 *   pool +0xa4 -> native_fn_022158a8 (image word 0x022158a8)
 *   pool +0xa8 -> native_fn_02215ac8 (image word 0x02215ac8)
 *   pool +0xac -> native_fn_02215dcc (image word 0x02215dcc)
 *   pool +0xb0 -> native_fn_02216290 (image word 0x02216290)
 *   pool +0xb4 -> native_fn_02216460 (image word 0x02216460)
 *   branch +0x14 -> +0x7c
 *   branch +0x18 -> +0x48
 *   branch +0x1c -> +0x50
 *   branch +0x20 -> +0x58
 *   branch +0x24 -> +0x58
 *   branch +0x28 -> +0x60
 *   branch +0x2c -> +0x68
 *   branch +0x30 -> +0x58
 *   branch +0x34 -> +0x58
 *   branch +0x38 -> +0x68
 *   branch +0x3c -> +0x68
 *   branch +0x40 -> +0x70
 *   branch +0x44 -> +0x78
 *   branch +0x4c -> +0x7c
 *   branch +0x54 -> +0x7c
 *   branch +0x5c -> +0x7c
 *   branch +0x64 -> +0x7c
 *   branch +0x6c -> +0x7c
 *   branch +0x74 -> +0x7c
 *   test +0x0c cmp r0, #11
 *   test +0x80 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02216554; the literal pool and
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

extern void native_fn_022154d8(void);
extern void native_fn_02215710(void);
extern void native_fn_022158a8(void);
extern void native_fn_02215ac8(void);
extern void native_fn_02215dcc(void);
extern void native_fn_02216290(void);
extern void native_fn_02216460(void);


asm u32 native_ov001_02216554 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02242ba0
    ldrb r0, [r0, #0x2]
    cmp r0, #11
    addls pc, pc, r0, lsl #2
    b ov001_02216554_L7c
    b ov001_02216554_L48
    b ov001_02216554_L50
    b ov001_02216554_L58
    b ov001_02216554_L58
    b ov001_02216554_L60
    b ov001_02216554_L68
    b ov001_02216554_L58
    b ov001_02216554_L58
    b ov001_02216554_L68
    b ov001_02216554_L68
    b ov001_02216554_L70
    b ov001_02216554_L78
ov001_02216554_L48:
    ldr r1, =native_fn_022154d8
    b ov001_02216554_L7c
ov001_02216554_L50:
    ldr r1, =native_fn_02215710
    b ov001_02216554_L7c
ov001_02216554_L58:
    ldr r1, =native_fn_022158a8
    b ov001_02216554_L7c
ov001_02216554_L60:
    ldr r1, =native_fn_02215ac8
    b ov001_02216554_L7c
ov001_02216554_L68:
    ldr r1, =native_fn_02215dcc
    b ov001_02216554_L7c
ov001_02216554_L70:
    ldr r1, =native_fn_02216290
    b ov001_02216554_L7c
ov001_02216554_L78:
    ldr r1, =native_fn_02216460
ov001_02216554_L7c:
    blx r1
    cmp r0, #0
    ldrne r0, =0x02242ba0
    movne r1, #3
    strne r1, [r0, #0x10]
    mov r0, #0
    ldmia sp!, {r3, pc}
}
