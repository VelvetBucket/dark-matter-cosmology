#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    exit 1
fi

template_dir="${1%/}"
original_dir="${template_dir}OG"

if [ ! -d "$template_dir" ]; then
    exit 1
fi

if [ -d "$original_dir" ]; then
    printf '%s\n' "template_files is already modified. No changes were made."
    exit 0
fi

if ! command -v patch >/dev/null 2>&1; then
    exit 1
fi

# Move the untouched original directory to template_filesOG.
mv "$template_dir" "$original_dir"

# Create a new template_files directory as an exact copy of template_filesOG.
if ! cp -a "$original_dir" "$template_dir"; then
    mv "$original_dir" "$template_dir"
    exit 1
fi

# Apply all known modifications only to the new template_files directory.
if ! patch -d "$template_dir" -p0 --batch --forward --no-backup-if-mismatch >/dev/null 2>&1 <<'PATCH_END'
--- b_sf_xxx_splitorders_fks.inc
+++ b_sf_xxx_splitorders_fks.inc
@@ -225,11 +225,10 @@
               ZTEMP = ZTEMP + CF(j,i)*JAMP2(J,M)
           ENDDO
 	  DO N = 1, NAMPSO
-              ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))
+              ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))/DENOM
           ENDDO
       ENDDO
     ENDDO
-    ANS(:) = ANS(:)/DENOM
     END
        
        
--- born_cnt_splitorders_fks.inc
+++ born_cnt_splitorders_fks.inc
@@ -321,14 +321,16 @@
             CF_INDEX = CF_INDEX +1
             ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)
           ENDDO
-	      DO N = 1, NAMPSO
+	  DO N = 1, NAMPSO
               BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))=BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))+ZTEMP*DCONJG(JAMP(I,N))   
           ENDDO
         ENDDO
+
+	  DO N = 1, NAMPSO
+              BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))=BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))/DENOM
+          ENDDO
+
         ENDDO
-        BORNS(:,:)=BORNS(:,:)/DENOM
-
-
 c        Do I = 1, NGRAPHS
 c          amp2(i)=amp2(i)+amp(i)*dconjg(amp(i))
 c        Enddo
@@ -354,8 +356,11 @@
           ENDDO
         ENDDO
       ENDDO
+
+	DO N = 1, NAMPSO
+        ANS(2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))= ANS(2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))/(2d0*DENOM) 
+        ENDDO
       ENDDO
-      ANS(2,:) = ANS(2,:) / (2d0*DENOM)
       nhel(glu_ij) = back_hel
       END
        
--- born_hel_splitorders_fks.inc
+++ born_hel_splitorders_fks.inc
@@ -200,7 +200,9 @@
       enddo
       endif
 %(jamp_lines)s
-    ANS(:) = 0d0
+    DO I = 1, NSQAMPSO
+    ANS(I) = 0d0
+    ENDDO
     DO M = 1, NAMPSO
       CF_INDEX = 0 
       DO I = 1, NCOLOR
@@ -211,8 +213,8 @@
           ENDDO
           ANS(SQSOINDEXB(M,M))=ANS(SQSOINDEXB(M,M))+ZTEMP*DCONJG(JAMP(I,M))
       ENDDO
+          ANS(SQSOINDEXB(M,M))=ANS(SQSOINDEXB(M,M))/DENOM
     ENDDO
-    ANS(:) = ANS(:)/DENOM
     END
        
        
--- bornmatrix_splitorders_fks.inc
+++ bornmatrix_splitorders_fks.inc
@@ -531,11 +531,17 @@
 C BEGIN CODE
 C ----------
       jamp(:,:) = (0d0,0d0)
-      borns(:,:) =0d0
-      ans(:,:) = (0d0, 0d0)
-
       glu_ij = ij_values(nfksprocess)
       if (force_ijglu_zero) glu_ij = 0
+
+      DO I = 1, NSQAMPSO
+        ANS(1,I)=0D0
+        ANS(2,I)=0D0
+        borns(1,I)=0d0
+        borns(2,I)=0d0
+      ENDDO
+      borns(1,0)=0d0
+      borns(2,0)=0d0
       if (glu_ij.ne.0) then
         back_hel = nhel(glu_ij)
         if (back_hel.ne.0) then
@@ -590,11 +596,14 @@
             CF_INDEX = CF_INDEX + 1
             ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)
           ENDDO
-	      DO N = 1, NAMPSO
+	  DO N = 1, NAMPSO
               BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))=BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP(I,N))   
           ENDDO
         ENDDO
-    ENDDO
+        DO N = 1, NAMPSO
+             BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))=BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))/DENOM
+        ENDDO
+        ENDDO
         Do I = 1, NGRAPHS
           amp2(i)=amp2(i)+amp(i)*dconjg(amp(i))
         Enddo
@@ -606,11 +615,10 @@
         ENDDO
       endif
       Enddo
-      borns(:,:) = borns(:,:)/DENOM
       do i = 1, nsqampso
       borns(1,0)=borns(1,0)+borns(1,i)
       borns(2,0)=borns(2,0)+borns(2,i)
-      ans(1,i) = borns(1,i) + borns(2,i)
+      ans(1,i) = borns(1,i) + borns(2,i) 
       enddo
       DO M = 1, NAMPSO
       CF_INDEX = 0
@@ -624,8 +632,10 @@
         ENDDO
       ENDDO
 
-      ENDDO
-      ANS(2,:) = ANS(2,:)/(2d0*DENOM)
+      DO N = 1, NAMPSO
+      ANS(2,SQSOINDEXB(M,N))= ANS(2,SQSOINDEXB(M,N))/(2d0*DENOM)
+      ENDDO
+      ENDDO
       if (glu_ij.ne.0) nhel(glu_ij) = back_hel
       END
        
--- cpp_process_class.inc
+++ cpp_process_class.inc
@@ -14,7 +14,7 @@
   virtual void initProc(string param_card_name); 
 
   // Calculate flavour-independent parts of cross section.
-  virtual void sigmaKin();
+  virtual double sigmaKin(double s, double theta);
 
   // Evaluate sigmaHat(sHat). 
   virtual double sigmaHat();
@@ -25,7 +25,9 @@
   virtual int    code()    const {return %(process_code)s;}
 
   const vector<double>& getMasses() const {return mME;}
-
+  const vector<double>& getNewMasses() const {return newMasses;}
+  const std::unordered_map<double, double> & getNewDOF() const {return newDOF;}
+  
   // Get and set momenta for matrix element evaluation
   vector<double*> getMomenta(){return p;}
   void setMomenta(vector<double*>& momenta){p = momenta;}
@@ -53,7 +55,13 @@
 
   // Pointer to the model parameters
   Parameters_%(model_name)s* pars;
-
+  
+  // vector with masses of new particles
+  vector<double> newMasses;
+  
+  // dictionary with dof of new particles
+  std::unordered_map<double, double> newDOF;
+  
   // vector with external particle masses
   vector<double> mME;
 
--- cpp_process_function_definitions.inc
+++ cpp_process_function_definitions.inc
@@ -11,28 +11,42 @@
     SLHAReader slha(param_card_name);
     pars->setIndependentParameters(slha);
     pars->setIndependentCouplings();
-    pars->printIndependentParameters();
-    pars->printIndependentCouplings();
+    //pars->printIndependentParameters();
+    //pars->printIndependentCouplings();
+    // Set masses and degrees of freedom of new particles
+    newMasses.push_back(pars->mdl_MN1); 
+    newDOF[pars->mdl_MN1] = 2.0;
+    newMasses.push_back(pars->mdl_MN2); 
+    newDOF[pars->mdl_MN2] = 2.0;
+    newMasses.push_back(pars->mdl_MN3); 
+    newDOF[pars->mdl_MN3] = 2.0;
+    newMasses.push_back(pars->mdl_MetR); 
+    newDOF[pars->mdl_MetR] = 2.0;
+    newMasses.push_back(pars->mdl_MetI); 
+    newDOF[pars->mdl_MetI] = 2.0;
+    newMasses.push_back(pars->mdl_Metp); 
+    newDOF[pars->mdl_Metp] = 2.0;
     %(initProc_lines)s
 } 
 
 //--------------------------------------------------------------------------
 // Evaluate |M|^2, part independent of incoming flavour. 
 
-void CPPProcess::sigmaKin() { 
+double CPPProcess::sigmaKin(double s, double theta) { 
     // Set the parameters which change event by event
     pars->setDependentParameters();
     pars->setDependentCouplings();
     static bool firsttime = true;
     if (firsttime){
-	pars->printDependentParameters();
-	pars->printDependentCouplings();
+	//pars->printDependentParameters();
+	//pars->printDependentCouplings();
 	firsttime = false;
     }
 
     // Reset color flows
     %(reset_jamp_lines)s
     %(sigmaKin_lines)s
+    
 }
 
 //--------------------------------------------------------------------------
--- cpp_process_h.inc
+++ cpp_process_h.inc
@@ -8,6 +8,7 @@
 
 #include <complex>
 #include <vector>
+#include <unordered_map>
 %(include_for_complex)s
 
 #include "Parameters_%(model_name)s.h"
--- cpp_process_sigmaKin_function.inc
+++ cpp_process_sigmaKin_function.inc
@@ -66,4 +66,4 @@
 for (int i=0;i < nprocesses; i++)
     matrix_element[i] /= denominators[i];
 
-
+return matrix_element[0] * std::sin(theta);
--- ewsudakov_goldstone_splitorders_fks.inc
+++ ewsudakov_goldstone_splitorders_fks.inc
@@ -186,7 +186,9 @@
 %(helas_calls)s
 %(jamp_lines)s
 
-    ANS(:) = 0d0
+    DO I = 1, NSQAMPSO
+    ANS(I) = 0d0
+    ENDDO
     DO M = 1, NAMPSO
       CF_INDEX = 0 
       DO I = 1, NCOLOR
@@ -196,11 +198,10 @@
               ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)
           ENDDO
 	  DO N = 1, NAMPSO
-              ANS(SQSOINDEXSDKG%(ime)d(M,N))=ANS(SQSOINDEXSDKG%(ime)d(M,N))+ZTEMP*DCONJG(JAMP(I,N))
+              ANS(SQSOINDEXSDKG%(ime)d(M,N))=ANS(SQSOINDEXSDKG%(ime)d(M,N))+ZTEMP*DCONJG(JAMP(I,N))/DENOM
           ENDDO
       ENDDO
     ENDDO
-    ANS(:) = ANS(:)/DENOM
     END
        
        
--- ewsudakov_pydispatcher.inc
+++ ewsudakov_pydispatcher.inc
@@ -1,5 +1,5 @@
 import importlib
-import sys, os
+import sys
 import numpy as np 
 
 # update the python path
@@ -7,21 +7,6 @@
 
 # the list of P0* directories
 pdir_list = [%(pdir_list)s]
-
-def import_lib(name):
-    old_dir = os.getcwd()
-    sys.path.insert(0, os.path.join('%(path)s',name))
-    try:
-        os.chdir(os.path.join('%(path)s',name))
-        out = importlib.import_module('ewsudpy_%%s' %% name)
-        os.chdir(old_dir)
-    except:
-        os.chdir(old_dir)
-        sys.path = sys.path[1:]
-        raise
-    return out
-
-
 
 # a dictionary which maps pdgs, in the format ((initial), (sorted final))
 # and the corresponding f2py modules
@@ -40,7 +25,7 @@
     p_transp =np.array([[pp[i] for pp in p] for i in range(4)], order='F')
     res = np.array([0.,0.,0.,0.,0.,0.], order='F')
 
-    res = pdg2ewsud_dict[pdgs].ewsudakov_py(p_transp,  g)
+    pdg2ewsud_dict[pdgs].ewsudakov_py(p_transp,  g, res)
 
     return res
 
--- ewsudakov_splitorders_fks.inc
+++ ewsudakov_splitorders_fks.inc
@@ -177,8 +177,9 @@
 %(helas_calls1)s
 %(jamp1_lines)s
 
-    ANS(:) = (0d0,0d0)
-
+    DO I = 1, NSQAMPSO
+    ANS(I) = (0d0,0d0)
+    ENDDO
 
 C Reshuffle the momenta here
 p_save(:,:) = p(:,:)
@@ -200,9 +201,11 @@
           DO J = 1, NCOLOR2
               ZTEMP = ZTEMP + CF(j,i)*JAMP2(J,M)
           ENDDO
+	  DO N = 1, NAMPSO
+              ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))/DENOM
+          ENDDO
       ENDDO
     ENDDO
-    ANS(:) = ANS(:) /DENOM
 C C NOT NEEDED
 C  include the imaginary factor if needed
 C     if (imag_power.ne.0) ans(:) = ans(:) * imag1**imag_power 
--- makefile_sa_f2py
+++ makefile_sa_f2py
@@ -9,52 +9,25 @@
 PROCESS=  allmatrix.o
 LIBRARY = libmatrix.a
 
-ifeq ($(strip $(HERE)),)
-    HERE := ./
-endif
-
-
-PROCNAME= $(notdir $(dir $(abspath $(HERE))))
-
 # For python linking (require f2py part of numpy)
 ifeq ($(origin MENUM),undefined)
   MENUM=2
 endif
 
-#%$(MENUM)py.so: %/matrix.f
-#	$(F2PY) --f77exec=$(FC) $(LINKLIBS_ME) -c $^ -m $(patsubst %/matrix.f,%$(MENUM)py,$^) --include-paths=$(HERE)/$(patsubst %/matrix.f,%,$^)
+%$(MENUM)py.so: %/matrix.f
+	$(F2PY) --f77exec=$(FC) $(LINKLIBS_ME) -c $^ -m $(patsubst %/matrix.f,%$(MENUM)py,$^) --include-paths=$(HERE)/$(patsubst %/matrix.f,%,$^) -I$(HERE)/$(patsubst %/matrix.f,%,$^)
 	
 	
-#all_matrix$(MENUM)py.so: $(LIBDIR)/$(LIBRARY) all_matrix.f
-#	$(F2PY) --f77exec=$(FC) $(LINKLIBS_ALL) -c all_matrix.f -m all_matrix$(MENUM)py --include-paths=$(HERE)
+all_matrix$(MENUM)py.so: $(LIBDIR)/$(LIBRARY) all_matrix.f
+	$(F2PY) --f77exec=$(FC) $(LINKLIBS_ALL) -c all_matrix.f -m all_matrix$(MENUM)py --include-paths=$(HERE) -I$(HERE)
 
     
-#allmatrix$(MENUM)py.so: $(patsubst %/matrix.f,%$(MENUM)py.so,$(wildcard */matrix.f)) all_matrix$(MENUM)py.so
-#	for lib in $(patsubst %.so,%,$^); do \
-#		printf "try:\n    from $$lib import *\nexcept:\n    from .$$lib import *\n" >> allmatrix$(MENUM)py.py; \
-#	done
+allmatrix$(MENUM)py.so: $(patsubst %/matrix.f,%$(MENUM)py.so,$(wildcard */matrix.f)) all_matrix$(MENUM)py.so
+	for lib in $(patsubst %.so,%,$^); do \
+		printf "try:\n    from $$lib import *\nexcept:\n    from .$$lib import *\n" >> allmatrix$(MENUM)py.py; \
+	done
 	
 	
-#$(LIBDIR)/$(LIBRARY): $(patsubst %.f,%.o,$(wildcard */matrix.f))  all_matrix.o
-#	$(call CREATELIB, $@, $^)  
+$(LIBDIR)/$(LIBRARY): $(patsubst %.f,%.o,$(wildcard */matrix.f))  all_matrix.o
+	$(call CREATELIB, $@, $^)  
 
-
-$(LIBDIR)/libdhelas.$(dylibext):
-	$(MAKE) -C "$(LIBDIR)/../Source/DHELAS" shared
-$(LIBDIR)/libmodel.$(dylibext):
-	$(MAKE) -C "$(LIBDIR)/../Source/MODEL" shared
-
-
-MATRIX_SRCS := $(wildcard */matrix.f)
-MATRIX_OBJS := $(patsubst %.f,%.o,$(wildcard */matrix.f))
-
-%/matrix.o: %/matrix.f
-	$(MAKE) -C $* matrix.o
-
-liball$(PROCNAME)_$(MENUM)me.$(dylibext): $(LIBDIR)/libdhelas.$(dylibext) $(LIBDIR)/libmodel.$(dylibext) all_matrix.o $(MATRIX_OBJS)
-	 $(FC) $(DYNLIBFLAG) $(RPATHFLAG)liball$(PROCNAME)_$(MENUM)me.$(dylibext) -o liball$(PROCNAME)_$(MENUM)me.$(dylibext) all_matrix.o */matrix.o ../Source/DHELAS/*.o ../Source/MODEL/*.o
-
-
-all_matrix$(MENUM)py.so:  liball$(PROCNAME)_$(MENUM)me.$(dylibext) f2py_wrapper.f makefile
-	LDFLAGS="-Wl,-rpath,$(HERE)" $(F2PY)  -c f2py_wrapper.f -L$(HERE) -lall$(PROCNAME)_$(MENUM)me $(LINKLIBS) -m                 all_matrix$(MENUM)py
-	touch all_matrix$(MENUM)py.so
--- makefile_sa_f_sp
+++ makefile_sa_f_sp
@@ -1,14 +1,11 @@
 include ../../Source/make_opts
-
 SHELL = /bin/bash
 HERE := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
-LIBDIR := $(abspath $(HERE)/../../lib)
-PDIR := $(strip $(notdir $(patsubst %/,%,$(strip $(HERE)))))
+LIBDIR = $(HERE)/../../lib/
 PROG   = check
 PROG_SPLITORDERS = check_sa_born_splitOrders
 LINKLIBS =  -L$(LIBDIR) -ldhelas -lmodel
-LIBS = $(LIBDIR)/libdhelas.$(libext) $(LIBDIR)/libmodel.$(libext)
-LIBS_SHARED = $(LIBDIR)/libdhelas.$(dylibext) $(LIBDIR)/libmodel.$(dylibext)
+LIBS = $(LIBDIR)libdhelas.$(libext) $(LIBDIR)libmodel.$(libext)
 PROCESS=  matrix.o
 CHECK_SA=  check_sa.o
 CHECK_SA_SPLITORDERS=  check_sa_born_splitOrders.o
@@ -26,19 +23,6 @@
   MENUM=2
 endif
 
-libme$(PDIR).$(dylibext): $(LIBDIR)/libdhelas.$(dylibext) $(LIBDIR)/libmodel.$(dylibext) matrix.o
-	gfortran $(DYNLIBFLAG) -o libme$(PDIR).$(dylibext) matrix.o ../../Source/DHELAS/*.o ../../Source/MODEL/*.o
-
-
-$(LIBDIR)/libdhelas.$(dylibext):
-	$(MAKE) -C "$(LIBDIR)/../Source/DHELAS" shared
-$(LIBDIR)/libmodel.$(dylibext):
-	$(MAKE) -C "$(LIBDIR)/../Source/MODEL" shared
-
-matrix$(MENUM)py.so: f2py_matrix_wrapper.f libme$(PDIR).$(dylibext)  makefile 
+matrix$(MENUM)py.so: matrix.f makefile $(LIBS)
 	touch __init__.py
-	LDFLAGS="-Wl,-rpath,$(HERE)" $(F2PY)  -c f2py_matrix_wrapper.f -L$(HERE) -lme$(PDIR) $(LINKLIBS) -m matrix$(MENUM)py 
-	touch matrix$(MENUM)py.so
-	cp $(LIBDIR)/*$(dylibext) .
-
-
+	$(F2PY) $(LINKLIBS) -c  matrix.f -m matrix$(MENUM)py --f77exec=$(FC) --include-paths=$(HERE) -I$(HERE)
--- matrix_standalone_matchbox_splitOrders_v4.inc
+++ matrix_standalone_matchbox_splitOrders_v4.inc
@@ -238,7 +238,7 @@
 %(helas_calls)s
 %(jamp_lines)s
 
-      RES(:) = 0.D0 
+      RES = 0.D0 
 	  DO M = 1, NAMPSO
         CF_INDEX = 0
         DO I = 1, NCOLOR
@@ -251,8 +251,11 @@
             RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N)) + ZTEMP*DCONJG(JAMP(I,N))
 		  ENDDO
         ENDDO
+		DO N = 1, NAMPSO
+            RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N))/DENOM
+		ENDDO
 	  ENDDO
-      RES(:) = RES(:)/DENOM
+
       END
 
       
--- matrix_standalone_splitOrders_v4.inc
+++ matrix_standalone_splitOrders_v4.inc
@@ -281,7 +281,7 @@
 %(helas_calls)s
 %(jamp_lines)s
 
-      RES(:) = 0.D0 
+      RES = 0.D0 
 	  DO M = 1, NAMPSO
         CF_INDEX= 0
         DO I = 1, NCOLOR
@@ -294,8 +294,10 @@
             RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N)) + REAL(ZTEMP*DCONJG(JAMP(I,N)))
 		  ENDDO
         ENDDO
+      DO N = 1, NAMPSO
+         RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N))/DENOM
+      ENDDO
 	  ENDDO
-      RES(:) = RES(:)/DENOM
       END
 
       SUBROUTINE %(proc_prefix)sGET_value(P, ALPHAS, NHEL ,ANS)
--- read_slha.cc
+++ read_slha.cc
@@ -30,8 +30,8 @@
   if(!param_card.good())
     throw "Error while opening param card";
 
-  if(verbose)
-    std::cout << "Opened slha file " << file_name << " for reading" << std::endl;
+  //if(verbose)
+  //  std::cout << "Opened slha file " << file_name << " for reading" << std::endl;
   char buf[200];
   std::string line;
   std::string block("");
--- realmatrix_splitorders_fks.inc
+++ realmatrix_splitorders_fks.inc
@@ -241,7 +241,9 @@
 %(helas_calls)s
 %(jamp_lines)s
 
-      RES(:) = 0d0
+      DO I=0,NSQAMPSO
+         RES(I)=0d0
+      ENDDO
       DO M = 1, NAMPSO
       CF_INDEX = 0
       DO I = 1, NCOLOR
@@ -255,8 +257,11 @@
           ENDDO
       ENDDO
 
-      ENDDO
-      RES(:) = RES(:)/DENOM
+	  DO N = 1, NAMPSO
+            RES(SQSOINDEX%(proc_prefix)s(M,N)) = RES(SQSOINDEX%(proc_prefix)s(M,N))/DENOM 
+          ENDDO
+      ENDDO
+
       DO I=1,NSQAMPSO
          RES(0)=RES(0)+RES(I)
       ENDDO
--- super_auto_dsig_group_v4.inc
+++ super_auto_dsig_group_v4.inc
@@ -1086,12 +1086,8 @@
 
     subroutine select_color(rcol, jamp2, iconfig, iproc, icol)
     implicit none
-    include 'nexternal.inc'
     include 'maxamps.inc' ! for the definition of maxflow
     include 'coloramps.inc' ! set the coloramps
-    include 'cluster.inc'
-    include 'genps.inc'
-    include 'run.inc'
 c    
 c   argument IN
 c
@@ -1113,11 +1109,6 @@
 	integer i,j
 	double precision xtarget
 
-    if (ickkw.gt.0) then
-        iconfig = igraphs(1)
-    endif   
-
-
       nc = int(jamp2(0))
       is_LC = .true.
       maxcolor=0
PATCH_END
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    exit 1
fi

# Ensure cpp_process_h.inc ends with exactly one final newline.
cpp_header="$template_dir/cpp_process_h.inc"
last_byte="$(tail -c 1 "$cpp_header" | od -An -t x1 | tr -d '[:space:]')"

if [ "$last_byte" != "0a" ]; then
    printf '\n' >> "$cpp_header"
fi

printf '%s\n' \
    "template_files modified successfully. Old template_files moved to template_filesOG."
