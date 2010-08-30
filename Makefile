#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= CSCI 5525 HW1
#Date		= 2010/08/24
#Description	= This file compiles the generated Python assembly code.

CC		= gcc
CFLAGS	= -O3 -march=native -Wall -m32 -lm
OBJS		= runtime.o hashtable.o hashtable_itr.o hashtable_utility.o

all: s

s: runtime.o
	for s in *.s; do \
		$(CC) $(CFLAGS) -o $${s%\.*} $$s $(OBJS); \
	done;

hashtable.o: hashtable.c hashtable.h hashtable_itr.o hashtable_utility.o
	$(CC) $(CFLAGS) -c $<

hashtable_itr.o: hashtable_itr.c hashtable_itr.h
	$(CC) $(CFLAGS) -c $<

hashtable_utility.o: hashtable_utility.c hashtable_utility.h
	$(CC) $(CFLAGS) -c $<

runtime: runtime.c runtime.h hashtable.o
	$(CC) $(CFLAGS) -c $<

.PHONY: clean
clean:
	rm -f *.o *.s
	rm -f *.pyc
