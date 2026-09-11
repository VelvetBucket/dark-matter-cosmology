LIBDIR=../lib
CXXFLAGS= -Ofast -I.
CXX=g++
target=$(LIBDIR)/libmodel_scotogenic_UFO.a

all: $(target)

objects=HelAmps_scotogenic_UFO.o Parameters_scotogenic_UFO.o rambo.o read_slha.o

$(target): $(objects)
	$(AR) cru $@ $(objects)
	ranlib $(target)

.PHONY: clean

clean:
	rm -f $(target)
	rm -f $(objects)

