LIBDIR=./lib
INCDIR=./src
MODELLIB=model_scotogenic_UFO
CXXFLAGS= -Ofast -I$(INCDIR) -I.
LIBFLAGS= -L$(LIBDIR) -l$(MODELLIB)

objects = ./main.o ./process/CPPProcess.o ./process/momenta.o ./tools/integration.o ./tools/bessel.o

check: $(objects) $(LIBDIR)/lib$(MODELLIB).a
	$(CXX) $(CXXFLAGS) -g -o $@ $(objects) $(LIBFLAGS) -lgsl -lgslcblas -lm

$(LIBDIR)/lib$(MODELLIB).a: $(INCDIR)/HelAmps_scotogenic_UFO.cc  $(INCDIR)/Parameters_scotogenic_UFO.cc $(INCDIR)/rambo.cc $(INCDIR)/read_slha.cc $(INCDIR)/HelAmps_scotogenic_UFO.h  $(INCDIR)/Parameters_scotogenic_UFO.h $(INCDIR)/rambo.h $(INCDIR)/read_slha.h
	make -C $(INCDIR)

./main.o: ./main.cpp ./process/CPPProcess.h ./process/momenta.h ./tools/tools.h 
	$(CXX) -c $(CXXFLAGS) -g -o $@ $<
	
./process/CPPProcess.o: ./process/CPPProcess.cc ./process/CPPProcess.h .FORCE
	$(CXX) -c $(CXXFLAGS) -g -o $@ $< $(LIBFLAGS)
	
./process/momenta.o: ./process/momenta.cc ./process/momenta.h
	$(CXX) -c $(CXXFLAGS) -g -o $@ $<

./tools/integration.o: ./tools/integration.cc ./tools/tools.h
	$(CXX) -c $(CXXFLAGS) -g -o $@ $< 
	
./tools/bessel.o: ./tools/bessel.cc ./tools/tools.h
	$(CXX) -c $(CXXFLAGS) -g -o $@ $<

.PHONY: clean .FORCE

.FORCE:

clean:
	rm -f main.o
	rm -f check 
	rm -f $(objects)

