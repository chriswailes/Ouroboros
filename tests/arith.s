# x86

# Functions

.globl main
.align 4
main:
	pushl %ebp            # 
	movl  %esp, %ebp      # 
	push  %ebx            # 
	push  %edi            # 
	push  %esi            # 

	movl  $0, %ebx        # 

	call  input_int       # 
	movl  $0, %edi        # 

	jmp   L9              # 
L8:



	testl $3, %edi        # 
	je    L5              # 

	andl  $-4, %edi       # 
	andl  $-4, %ebx       # 
	pushl %ebx            # 
	pushl %edi            # 
	call  add             # 
	addl  $8, %esp        # 
	orl   $3, %eax        # 
	orl   $3, %edi        # 
	orl   $3, %ebx        # 
	movl  %eax, %edi      # 
	jmp   L4              # 
L5:

	sarl  $2, %edi        # 
	sarl  $2, %ebx        # 
	addl  %ebx, %edi      # 
	sall  $2, %edi        # 
	sall  $2, %ebx        # 
L4:

	movl  %ebx, %eax      # 
	sarl  $2, %eax        # 
	negl  %eax            # 
	sall  $2, %eax        # 


	testl $3, %edi        # 
	je    L7              # 

	andl  $-4, %eax       # 
	andl  $-4, %edi       # 
	pushl %edi            # 
	pushl %eax            # 
	call  add             # 
	addl  $8, %esp        # 
	orl   $3, %eax        # 
	orl   $3, %edi        # 
	movl  %eax, %edi      # 
	jmp   L6              # 
L7:

	sarl  $2, %eax        # 
	sarl  $2, %edi        # 
	addl  %eax, %edi      # 
	sall  $2, %edi        # 
	sall  $2, %eax        # 
L6:

	sarl  $2, %ebx        # 
	incl  %ebx            # 
	sall  $2, %ebx        # 
L9:


	movl  %ebx, %esi      # 

	testl $3, %esi        # 
	je    L3              # 

	andl  $-4, %esi       # 
	andl  $-4, %eax       # 
	pushl %eax            # 
	pushl %esi            # 
	call  not_equal       # 
	addl  $8, %esp        # 
	sall  $2, %eax        # 
	orl   $1, %eax        # 
	sall  $2, %esi        # 
	movl  %eax, %esi      # 
	jmp   L2              # 
L3:

	cmpl  %esi, %eax      # 
	je    L1              # 
	movl  $5, %esi        # 
	jmp   L0              # 
L1:
	movl  $1, %esi        # 
L0:
L2:
	cmpl  $1, %esi        # 
	jg    L8              # 

	pushl %edi            # 
	call  print_any       # 
	addl  $4, %esp        # 

	pop   %esi            # 
	pop   %edi            # 
	pop   %ebx            # 
	leave                 # 
	ret                   # 
