/* ov006 row 0x021fa484: 412 bytes.
 *
 * What it does: 172 instructions; 26 call(s) to 0x021fa620, 0x02203ebc, 0x021fa67c, +23 more; loops (back edge at +0x4c); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x18c -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x190 -> native_fn_021fa980+1 (image word 0x021fa981)
 *   pool +0x194 -> native_fn_021fb414+1 (image word 0x021fb415)
 *   pool +0x198 -> native_fn_021fb39c+1 (image word 0x021fb39d)
 *   branch +0x0a -> +0x70
 *   branch +0x12 -> +0x70
 *   branch +0x1a -> +0x70
 *   branch +0x24 -> +0x30
 *   branch +0x38 -> +0x52
 *   branch +0x5c -> +0x9e
 *   branch +0x64 -> +0x84
 *   branch +0x6e -> +0x72
 *   branch +0x70 -> +0x18a
 *   branch +0xa8 -> +0xb6
 *   branch +0xc0 -> +0x100
 *   branch +0xc8 -> +0xe6
 *   branch +0xd2 -> +0x18a
 *   branch +0x10a -> +0x118
 *   branch +0x120 -> +0x12a
 *   branch +0x132 -> +0x140
 *   branch +0x148 -> +0x152
 *   branch +0x15a -> +0x168
 *   branch +0x170 -> +0x17a
 *   branch +0x182 -> +0x18a
 *   test +0x08 cmp r0, #0x0
 *   test +0x10 cmp r0, #0x0
 *   test +0x18 cmp r0, #0x0
 *   test +0x22 cmp r0, #0x0
 *   test +0x36 cmp r0, #0x0
 *   test +0x5a cmp r0, #0x0
 *   test +0x62 cmp r1, #0x91
 *   test +0x6c cmp r0, #0x0
 *   test +0xa6 cmp r0, #0x0
 *   test +0xbe cmp r0, #0x0
 *   test +0xc6 cmp r1, #0x0
 *   test +0xd0 cmp r0, #0x0
 *   test +0x108 cmp r0, #0x0
 *   test +0x11e cmp r0, #0x0
 *   test +0x130 cmp r0, #0x0
 *   test +0x146 cmp r0, #0x0
 *   test +0x158 cmp r0, #0x0
 *   test +0x16e cmp r0, #0x0
 *   test +0x180 cmp r0, #0x0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fa484; the literal pool and
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

extern void native_fn_021fa620(void);
extern void native_fn_02203ebc(void);
extern void native_fn_021fa67c(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_021fa980(void);
extern void native_fn_021f52cc(void);
extern void native_fn_02203eec(void);
extern void native_fn_021fb414(void);
extern void native_fn_0220490c(void);
extern void native_fn_02203f1c(void);
extern void native_fn_021fb39c(void);
extern void native_fn_021fb5e4(void);


asm u32 native_ov006_021fa484 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c0ec
    ldr r1, [r0, #0x8]
    ldr r0, [r1, #0x38]
    cmp r0, #0x0
    bne ov006_021fa484_L70
    add r1, #0x45
    ldrb r0, [r1, #0]
    cmp r0, #0x0
    bne ov006_021fa484_L70
    bl native_fn_021fa620
    cmp r0, #0x0
    bne ov006_021fa484_L70
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021fa484_L30
    ldr r0, =0x0221c0ec
    ldrb r0, [r0, #0]
    bl native_fn_021fa67c
    pop {r3, pc}
ov006_021fa484_L30:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021fa484_L52
    mov r0, #0x7
    bl native_fn_021ff6d4
    ldr r0, =0x0221c0ec
    mov r1, #0xd
    ldr r0, [r0, #0x8]
    add r0, #0x40
    strb r1, [r0, #0]
    ldr r0, =native_fn_021fa980+1
    bl native_fn_021f52cc
    pop {r3, pc}
ov006_021fa484_L52:
    mov r0, #0x2
    lsl r0, r0, #0x8
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fa484_L9e
    ldr r0, =0x0221c0ec
    ldrh r1, [r0, #0x4]
    cmp r1, #0x91
    bne ov006_021fa484_L84
    ldr r0, [r0, #0x8]
    add r0, #0x47
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021fa484_L72
ov006_021fa484_L70:
    b ov006_021fa484_L18a
ov006_021fa484_L72:
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c0ec
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021fa484_L84:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, =native_fn_021fb414+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c0ec
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, pc}
ov006_021fa484_L9e:
    mov r0, #0x2
    lsl r0, r0, #0x8
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021fa484_Lb6
    ldr r0, =0x0221c0ec
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021fa484_Lb6:
    mov r0, #0x1
    lsl r0, r0, #0x8
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fa484_L100
    ldr r0, =0x0221c0ec
    ldrh r1, [r0, #0x4]
    cmp r1, #0x0
    bne ov006_021fa484_Le6
    ldr r0, [r0, #0x8]
    add r0, #0x47
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021fa484_L18a
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, =0x0221c0ec
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021fa484_Le6:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, =native_fn_021fb39c+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =0x0221c0ec
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, pc}
ov006_021fa484_L100:
    mov r0, #0x1
    lsl r0, r0, #0x8
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021fa484_L118
    ldr r0, =0x0221c0ec
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021fa484_L118:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fa484_L12a
    mov r0, #0x1
    bl native_fn_021fb5e4
    pop {r3, pc}
ov006_021fa484_L12a:
    mov r0, #0x40
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021fa484_L140
    ldr r0, =0x0221c0ec
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021fa484_L140:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fa484_L152
    mov r0, #0x3
    bl native_fn_021fb5e4
    pop {r3, pc}
ov006_021fa484_L152:
    mov r0, #0x80
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq ov006_021fa484_L168
    ldr r0, =0x0221c0ec
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, pc}
ov006_021fa484_L168:
    mov r0, #0x20
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fa484_L17a
    mov r0, #0x0
    bl native_fn_021fb5e4
    pop {r3, pc}
ov006_021fa484_L17a:
    mov r0, #0x10
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fa484_L18a
    mov r0, #0x2
    bl native_fn_021fb5e4
ov006_021fa484_L18a:
    pop {r3, pc}
}
