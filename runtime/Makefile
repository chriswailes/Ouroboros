#Author		= Chris Wailes <chris.wailes@gmail.com
#Project		= CSCI 5525 HW1
#Date		= 2010/09/01
#Description	= This file compiles our runtime code.

AR		= ar
CC		= gcc

AFLAGS	= rcs
CFLAGS	= -O3 -Wall -fPIC $(CONDFLAGS)
LFAGS	= -lm
SFLAGS	= -shared -Wl,-soname,libpyrun.so

OBJS		= runtime.o hashtable.o hashtable_itr.o hashtable_utility.o

all: static

hashtable.o: hashtable.c hashtable.h hashtable_itr.o hashtable_utility.o
	$(CC) $(CFLAGS) -c $<

hashtable_itr.o: hashtable_itr.c hashtable_itr.h
	$(CC) $(CFLAGS) -c $<

hashtable_utility.o: hashtable_utility.c hashtable_utility.h
	$(CC) $(CFLAGS) -c $<

shared: runtime.o
	$(CC) $(CFLAGS) $(SFLAGS) -o libpyrun.so $(OBJS)

static: runtime.o
	$(AR) $(AFLAGS) libpyrun.a $(OBJS)
	
runtime.o: runtime.c runtime.h hashtable.o
	$(CC) $(CFLAGS) -c $<

.PHONY: clean
clean:
	rm -f *.o *.a *.sa
