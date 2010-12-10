#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= CSCI 5525 HW1
#Date		= 2010/09/01
#Description	= This file compiles our runtime code.

AR		= ar
CC		= gcc

AFLAGS	= rcs
CFLAGS	= -O3 -Wall -fPIC -march=native
LFAGS	= -lm
SFLAGS	= -shared -Wl,-soname,libpyrun.so

CFLAGS32	= $(CFLAGS) -m32
CFLAGS64	= $(CLFAGS) -m64

OBJS32	= runtime-32.o hashtable-32.o hashtable_itr-32.o hashtable_utility-32.o
OBJS64	= runtime-64.o hashtable-64.o hashtable_itr-64.o hashtable_utility-64.o

all: static-32 static-64

##################
# 32-Bit Objects #
##################

hashtable-32.o: hashtable.c hashtable.h hashtable_itr-32.o hashtable_utility-32.o
	$(CC) $(CFLAGS32) -c -o $@ $<

hashtable_itr-32.o: hashtable_itr.c hashtable_itr.h
	$(CC) $(CFLAGS32) -c -o $@ $<

hashtable_utility-32.o: hashtable_utility.c hashtable_utility.h
	$(CC) $(CFLAGS32) -c -o $@ $<

shared-32: runtime-32.o
	$(CC) $(CFLAGS32) $(SFLAGS) -o libpyrun32.so $(OBJS32)

static-32: runtime-32.o
	$(AR) $(AFLAGS) libpyrun32.a $(OBJS32)
	
runtime-32.o: runtime.c runtime.h hashtable-32.o
	$(CC) $(CFLAGS32) -c -o $@ $<

##################
# 64-Bit Objects #
##################

hashtable-64.o: hashtable.c hashtable.h hashtable_itr-64.o hashtable_utility-64.o
	$(CC) $(CFLAGS64) -c -o $@ $<

hashtable_itr-64.o: hashtable_itr.c hashtable_itr.h
	$(CC) $(CFLAGS64) -c -o $@ $<

hashtable_utility-64.o: hashtable_utility.c hashtable_utility.h
	$(CC) $(CFLAGS64) -c -o $@ $<

shared-64: runtime-64.o
	$(CC) $(CFLAGS64) $(SFLAGS) -o libpyrun64.so $(OBJS64)

static-64: runtime-64.o
	$(AR) $(AFLAGS) libpyrun64.a $(OBJS64)
	
runtime-64.o: runtime.c runtime.h hashtable-64.o
	$(CC) $(CFLAGS64) -c -o $@ $<

.PHONY: clean
clean:
	rm -f *.o *.a *.so
