/* ov006 row 0x022018bc: 112 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x6c -> native_fn_0220192c+1 (image word 0x0220192d)
 *   branch +0x0e -> +0x20
 *   branch +0x22 -> +0x34
 *   branch +0x3e -> +0x5c
 *   branch +0x4a -> +0x50
 *   back edge +0x5a -> +0x42
 *   test +0x0c cmp r0, r1
 *   test +0x20 cmp r0, #0x0
 *   test +0x3c tst r1, r0
 *   test +0x48 cmp r4, #0x10
 *   test +0x58 tst r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022018bc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02012290(void);
extern void native_fn_022012c0(void);
extern void native_fn_02201270(void);
extern void native_fn_0220192c(void);
extern void native_fn_022019bc(void);


asm u32 native_ov006_022018bc (register u32 a0)
{
    push {r4, lr}
    add r4, r0, #0x0
    blx native_fn_02012290
    mov r1, #0x2
    lsl r1, r1, #0xe
    cmp r0, r1
    bne ov006_022018bc_L20
    mov r0, #0x3
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    mov r0, #0x3
    pop {r4, pc}
ov006_022018bc_L20:
    cmp r0, #0x0
    bne ov006_022018bc_L34
    mov r0, #0x16
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    mov r0, #0x18
    pop {r4, pc}
ov006_022018bc_L34:
    mov r2, #0x1
    sub r1, r4, #0x1
    lsl r2, r1
    add r1, r2, #0x0
    tst r1, r0
    bne ov006_022018bc_L5c
    mov r2, #0x1
ov006_022018bc_L42:
    add r1, r4, #0x1
    lsl r1, r1, #0x10
    lsr r4, r1, #0x10
    cmp r4, #0x10
    bls ov006_022018bc_L50
    mov r0, #0x18
    pop {r4, pc}
ov006_022018bc_L50:
    sub r1, r4, #0x1
    add r3, r2, #0x0
    lsl r3, r1
    add r1, r3, #0x0
    tst r1, r0
    beq ov006_022018bc_L42
ov006_022018bc_L5c:
    ldr r0, =native_fn_0220192c+1
    add r1, r4, #0x0
    bl native_fn_022019bc
    lsl r0, r0, #0x10
    lsr r0, r0, #0x10
    pop {r4, pc}
    mov r8, r8
}
