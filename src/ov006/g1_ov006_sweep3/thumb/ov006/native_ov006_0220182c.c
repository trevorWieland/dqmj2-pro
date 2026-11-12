/* ov006 row 0x0220182c: 144 bytes.
 *
 * What it does: 57 instructions; 7 call(s) to 0x020081fc, 0x02201270, 0x022018bc, +4 more; loops (back edge at +0x06); returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x80 -> constant 0x027ffc3c (image word 0x027ffc3c)
 *   pool +0x84 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0x88 -> constant 0x00010dcd (image word 0x00010dcd)
 *   pool +0x8c -> constant 0x00003039 (image word 0x00003039)
 *   branch +0x50 -> +0x64
 *   branch +0x66 -> +0x78
 *   test +0x4e cmp r0, #0x18
 *   test +0x64 cmp r0, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220182c; the literal pool and
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

extern void native_fn_020081fc(void);
extern void native_fn_02201270(void);
extern void native_fn_022018bc(void);
extern void native_fn_022012c0(void);


asm u32 native_ov006_0220182c (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x8
    add r0, sp, #0x0
    blx native_fn_020081fc
    ldr r0, =0x027ffc3c
    ldr r3, [r0, #0]
    add r0, sp, #0x0
    ldrh r2, [r0, #0x4]
    ldrh r1, [r0, #0x2]
    ldrh r0, [r0, #0]
    add r0, r0, r3
    add r0, r1, r0
    ldr r1, =0x0221c164
    add r2, r2, r0
    ldr r0, [r1, #0x4]
    str r2, [r0, #0x58]
    ldr r4, [r1, #0x4]
    ldr r0, =0x00010dcd
    ldr r2, [r4, #0x58]
    add r3, r2, #0x0
    mul r3, r0
    ldr r0, =0x00003039
    mov r2, #0x0
    add r0, r3, r0
    str r0, [r4, #0x58]
    ldr r0, [r1, #0x4]
    add r0, #0x5c
    strh r2, [r0, #0]
    ldr r0, [r1, #0x4]
    mov r2, #0x65
    add r0, #0x5e
    strh r2, [r0, #0]
    mov r0, #0x3
    bl native_fn_02201270
    mov r0, #0x1
    bl native_fn_022018bc
    cmp r0, #0x18
    bne ov006_0220182c_L64
    mov r0, #0x18
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    add sp, #0x8
    mov r0, #0x0
    pop {r4, pc}
ov006_0220182c_L64:
    cmp r0, #0x2
    beq ov006_0220182c_L78
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    add sp, #0x8
    mov r0, #0x0
    pop {r4, pc}
ov006_0220182c_L78:
    mov r0, #0x1
    add sp, #0x8
    pop {r4, pc}
    mov r8, r8
}
