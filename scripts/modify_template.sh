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

read_file() {
    cat "$1"
    printf '\034'
}

replace_block() {
    local file="$1"
    local old="$2"
    local new="$3"
    local content

    content="$(read_file "$file")"
    content="${content%$'\034'}"

    if [[ "$content" != *"$old"* ]]; then
        return 1
    fi

    content="${content/"$old"/"$new"}"
    printf '%s' "$content" > "$file"
}

# ============================================
# Check whether template_files is already modified
# ============================================

is_modified=true

# 1. b_sf_xxx_splitorders_fks.inc
grep -Fq 'ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))/DENOM' \
    "$template_dir/b_sf_xxx_splitorders_fks.inc" || is_modified=false

# 2. born_cnt_splitorders_fks.inc
grep -Fq 'BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))=BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))/DENOM' \
    "$template_dir/born_cnt_splitorders_fks.inc" || is_modified=false
grep -Fq 'ANS(2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))= ANS(2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))/(2d0*DENOM)' \
    "$template_dir/born_cnt_splitorders_fks.inc" || is_modified=false

# 3. born_hel_splitorders_fks.inc
grep -Fq 'DO I = 1, NSQAMPSO' \
    "$template_dir/born_hel_splitorders_fks.inc" || is_modified=false
grep -Fq 'ANS(SQSOINDEXB(M,M))=ANS(SQSOINDEXB(M,M))/DENOM' \
    "$template_dir/born_hel_splitorders_fks.inc" || is_modified=false

# 4. bornmatrix_splitorders_fks.inc
grep -Fq 'borns(1,0)=0d0' \
    "$template_dir/bornmatrix_splitorders_fks.inc" || is_modified=false
grep -Fq 'BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))=BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))/DENOM' \
    "$template_dir/bornmatrix_splitorders_fks.inc" || is_modified=false
grep -Fq 'ANS(2,SQSOINDEXB(M,N))= ANS(2,SQSOINDEXB(M,N))/(2d0*DENOM)' \
    "$template_dir/bornmatrix_splitorders_fks.inc" || is_modified=false

# 5. cpp_process_class.inc
grep -Fq 'virtual double sigmaKin(double s, double theta);' \
    "$template_dir/cpp_process_class.inc" || is_modified=false
grep -Fq 'getNewMasses() const {return newMasses;}' \
    "$template_dir/cpp_process_class.inc" || is_modified=false
grep -Fq 'std::unordered_map<double, double> newDOF;' \
    "$template_dir/cpp_process_class.inc" || is_modified=false

# 6. cpp_process_function_definitions.inc
grep -Fq '//pars->printIndependentParameters();' \
    "$template_dir/cpp_process_function_definitions.inc" || is_modified=false
grep -Fq 'newMasses.push_back(pars->mdl_MN1);' \
    "$template_dir/cpp_process_function_definitions.inc" || is_modified=false
grep -Fq 'double CPPProcess::sigmaKin(double s, double theta)' \
    "$template_dir/cpp_process_function_definitions.inc" || is_modified=false
grep -Fq '//pars->printDependentParameters();' \
    "$template_dir/cpp_process_function_definitions.inc" || is_modified=false

# 7. cpp_process_h.inc
grep -Fq '#include <unordered_map>' \
    "$template_dir/cpp_process_h.inc" || is_modified=false

# 8. cpp_process_sigmaKin_function.inc
grep -Fq 'return matrix_element[0] * std::sin(theta);' \
    "$template_dir/cpp_process_sigmaKin_function.inc" || is_modified=false

# 9. ewsudakov_goldstone_splitorders_fks.inc
grep -Fq 'ANS(SQSOINDEXSDKG%(ime)d(M,N))=ANS(SQSOINDEXSDKG%(ime)d(M,N))+ZTEMP*DCONJG(JAMP(I,N))/DENOM' \
    "$template_dir/ewsudakov_goldstone_splitorders_fks.inc" || is_modified=false

# 10. ewsudakov_pydispatcher.inc
grep -Fq 'import sys' \
    "$template_dir/ewsudakov_pydispatcher.inc" || is_modified=false
grep -Fq 'pdg2ewsud_dict[pdgs].ewsudakov_py(p_transp,  g, res)' \
    "$template_dir/ewsudakov_pydispatcher.inc" || is_modified=false
if grep -Fq 'def import_lib(name):' "$template_dir/ewsudakov_pydispatcher.inc"; then
    is_modified=false
fi

# 11. ewsudakov_splitorders_fks.inc
grep -Fq 'ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))/DENOM' \
    "$template_dir/ewsudakov_splitorders_fks.inc" || is_modified=false

# 12. makefile_sa_f2py
grep -Fq -e '--include-paths=$(HERE)/$(patsubst %/matrix.f,%,$^) -I$(HERE)/$(patsubst %/matrix.f,%,$^)' \
    "$template_dir/makefile_sa_f2py" || is_modified=false
grep -Fq 'allmatrix$(MENUM)py.so:' \
    "$template_dir/makefile_sa_f2py" || is_modified=false
grep -Fq '$(LIBDIR)/$(LIBRARY):' \
    "$template_dir/makefile_sa_f2py" || is_modified=false
if grep -Fq 'PROCNAME=' "$template_dir/makefile_sa_f2py"; then
    is_modified=false
fi

# 13. makefile_sa_f_sp
grep -Fq 'LIBDIR = $(HERE)/../../lib/' \
    "$template_dir/makefile_sa_f_sp" || is_modified=false
grep -Fq 'matrix$(MENUM)py.so: matrix.f makefile $(LIBS)' \
    "$template_dir/makefile_sa_f_sp" || is_modified=false
if grep -Fq 'PDIR :=' "$template_dir/makefile_sa_f_sp"; then
    is_modified=false
fi

# 14. matrix_standalone_matchbox_splitOrders_v4.inc
grep -Fq 'RES = 0.D0' \
    "$template_dir/matrix_standalone_matchbox_splitOrders_v4.inc" || is_modified=false
grep -Fq 'RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N))/DENOM' \
    "$template_dir/matrix_standalone_matchbox_splitOrders_v4.inc" || is_modified=false

# 15. matrix_standalone_splitOrders_v4.inc
grep -Fq 'RES = 0.D0' \
    "$template_dir/matrix_standalone_splitOrders_v4.inc" || is_modified=false
grep -Fq 'RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N))/DENOM' \
    "$template_dir/matrix_standalone_splitOrders_v4.inc" || is_modified=false

# 16. read_slha.cc
grep -Fq '//if(verbose)' \
    "$template_dir/read_slha.cc" || is_modified=false
grep -Fq '//  std::cout << "Opened slha file "' \
    "$template_dir/read_slha.cc" || is_modified=false

# 17. realmatrix_splitorders_fks.inc
grep -Fq 'DO I=0,NSQAMPSO' \
    "$template_dir/realmatrix_splitorders_fks.inc" || is_modified=false
grep -Fq 'RES(SQSOINDEX%(proc_prefix)s(M,N)) = RES(SQSOINDEX%(proc_prefix)s(M,N))/DENOM' \
    "$template_dir/realmatrix_splitorders_fks.inc" || is_modified=false

# 18. super_auto_dsig_group_v4.inc
select_color_block="$(
    grep -F -A 40 'subroutine select_color(rcol, jamp2, iconfig, iproc, icol)' \
        "$template_dir/super_auto_dsig_group_v4.inc" || true
)"

if [ -z "$select_color_block" ]; then
    is_modified=false
fi

if printf '%s\n' "$select_color_block" | grep -Fq "include 'nexternal.inc'"; then
    is_modified=false
fi

if printf '%s\n' "$select_color_block" | grep -Fq "include 'cluster.inc'"; then
    is_modified=false
fi

if printf '%s\n' "$select_color_block" | grep -Fq "include 'genps.inc'"; then
    is_modified=false
fi

if printf '%s\n' "$select_color_block" | grep -Fq "include 'run.inc'"; then
    is_modified=false
fi

if printf '%s\n' "$select_color_block" | grep -Fq 'if (ickkw.gt.0) then'; then
    is_modified=false
fi

if [ "$is_modified" = true ]; then
    printf '%s\n' \
        "template_files is already modified. No changes were made."
    exit 0
fi

if [ -e "$original_dir" ]; then
    printf '%s\n' "template_filesOG already exists, but template_files is not fully modified. No changes were made." >&2
    exit 1
fi

mv "$template_dir" "$original_dir"

if ! cp -a "$original_dir" "$template_dir"; then
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to copy template_files. The original directory was restored." >&2
    exit 1
fi

# Apply the known modifications directly.

if ! replace_block "$template_dir/b_sf_xxx_splitorders_fks.inc" \
    $'              ZTEMP = ZTEMP + CF(j,i)*JAMP2(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))\n          ENDDO\n      ENDDO\n    ENDDO\n    ANS(:) = ANS(:)/DENOM\n    END\n       \n       \n' \
    $'              ZTEMP = ZTEMP + CF(j,i)*JAMP2(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))/DENOM\n          ENDDO\n      ENDDO\n    ENDDO\n    END\n       \n       \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/born_cnt_splitorders_fks.inc" \
    $'            CF_INDEX = CF_INDEX +1\n            ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)\n          ENDDO\n\t      DO N = 1, NAMPSO\n              BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))=BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))+ZTEMP*DCONJG(JAMP(I,N))   \n          ENDDO\n        ENDDO\n        ENDDO\n        BORNS(:,:)=BORNS(:,:)/DENOM\n\n\nc        Do I = 1, NGRAPHS\nc          amp2(i)=amp2(i)+amp(i)*dconjg(amp(i))\nc        Enddo\n' \
    $'            CF_INDEX = CF_INDEX +1\n            ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))=BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))+ZTEMP*DCONJG(JAMP(I,N))   \n          ENDDO\n        ENDDO\n\n\t  DO N = 1, NAMPSO\n              BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))=BORNS(2-(1-ihel)/2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))/DENOM\n          ENDDO\n\n        ENDDO\nc        Do I = 1, NGRAPHS\nc          amp2(i)=amp2(i)+amp(i)*dconjg(amp(i))\nc        Enddo\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/born_cnt_splitorders_fks.inc" \
    $'          ENDDO\n        ENDDO\n      ENDDO\n      ENDDO\n      ANS(2,:) = ANS(2,:) / (2d0*DENOM)\n      nhel(glu_ij) = back_hel\n      END\n       \n' \
    $'          ENDDO\n        ENDDO\n      ENDDO\n\n\tDO N = 1, NAMPSO\n        ANS(2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))= ANS(2,SQSOINDEXB_CNT%(proc_prefix)s(M,N))/(2d0*DENOM) \n        ENDDO\n      ENDDO\n      nhel(glu_ij) = back_hel\n      END\n       \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/born_hel_splitorders_fks.inc" \
    $'      enddo\n      endif\n%(jamp_lines)s\n    ANS(:) = 0d0\n    DO M = 1, NAMPSO\n      CF_INDEX = 0 \n      DO I = 1, NCOLOR\n' \
    $'      enddo\n      endif\n%(jamp_lines)s\n    DO I = 1, NSQAMPSO\n    ANS(I) = 0d0\n    ENDDO\n    DO M = 1, NAMPSO\n      CF_INDEX = 0 \n      DO I = 1, NCOLOR\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/born_hel_splitorders_fks.inc" \
    $'          ENDDO\n          ANS(SQSOINDEXB(M,M))=ANS(SQSOINDEXB(M,M))+ZTEMP*DCONJG(JAMP(I,M))\n      ENDDO\n    ENDDO\n    ANS(:) = ANS(:)/DENOM\n    END\n       \n       \n' \
    $'          ENDDO\n          ANS(SQSOINDEXB(M,M))=ANS(SQSOINDEXB(M,M))+ZTEMP*DCONJG(JAMP(I,M))\n      ENDDO\n          ANS(SQSOINDEXB(M,M))=ANS(SQSOINDEXB(M,M))/DENOM\n    ENDDO\n    END\n       \n       \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/bornmatrix_splitorders_fks.inc" \
    $'C BEGIN CODE\nC ----------\n      jamp(:,:) = (0d0,0d0)\n      borns(:,:) =0d0\n      ans(:,:) = (0d0, 0d0)\n\n      glu_ij = ij_values(nfksprocess)\n      if (force_ijglu_zero) glu_ij = 0\n      if (glu_ij.ne.0) then\n        back_hel = nhel(glu_ij)\n        if (back_hel.ne.0) then\n' \
    $'C BEGIN CODE\nC ----------\n      jamp(:,:) = (0d0,0d0)\n      glu_ij = ij_values(nfksprocess)\n      if (force_ijglu_zero) glu_ij = 0\n\n      DO I = 1, NSQAMPSO\n        ANS(1,I)=0D0\n        ANS(2,I)=0D0\n        borns(1,I)=0d0\n        borns(2,I)=0d0\n      ENDDO\n      borns(1,0)=0d0\n      borns(2,0)=0d0\n      if (glu_ij.ne.0) then\n        back_hel = nhel(glu_ij)\n        if (back_hel.ne.0) then\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/bornmatrix_splitorders_fks.inc" \
    $'            CF_INDEX = CF_INDEX + 1\n            ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)\n          ENDDO\n\t      DO N = 1, NAMPSO\n              BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))=BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP(I,N))   \n          ENDDO\n        ENDDO\n    ENDDO\n        Do I = 1, NGRAPHS\n          amp2(i)=amp2(i)+amp(i)*dconjg(amp(i))\n        Enddo\n' \
    $'            CF_INDEX = CF_INDEX + 1\n            ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))=BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP(I,N))   \n          ENDDO\n        ENDDO\n        DO N = 1, NAMPSO\n             BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))=BORNS(2-(1+back_hel*ihel)/2,SQSOINDEXB(M,N))/DENOM\n        ENDDO\n        ENDDO\n        Do I = 1, NGRAPHS\n          amp2(i)=amp2(i)+amp(i)*dconjg(amp(i))\n        Enddo\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/bornmatrix_splitorders_fks.inc" \
    $'        ENDDO\n      endif\n      Enddo\n      borns(:,:) = borns(:,:)/DENOM\n      do i = 1, nsqampso\n      borns(1,0)=borns(1,0)+borns(1,i)\n      borns(2,0)=borns(2,0)+borns(2,i)\n      ans(1,i) = borns(1,i) + borns(2,i)\n      enddo\n      DO M = 1, NAMPSO\n      CF_INDEX = 0\n' \
    $'        ENDDO\n      endif\n      Enddo\n      do i = 1, nsqampso\n      borns(1,0)=borns(1,0)+borns(1,i)\n      borns(2,0)=borns(2,0)+borns(2,i)\n      ans(1,i) = borns(1,i) + borns(2,i) \n      enddo\n      DO M = 1, NAMPSO\n      CF_INDEX = 0\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/bornmatrix_splitorders_fks.inc" \
    $'        ENDDO\n      ENDDO\n\n      ENDDO\n      ANS(2,:) = ANS(2,:)/(2d0*DENOM)\n      if (glu_ij.ne.0) nhel(glu_ij) = back_hel\n      END\n       \n' \
    $'        ENDDO\n      ENDDO\n\n      DO N = 1, NAMPSO\n      ANS(2,SQSOINDEXB(M,N))= ANS(2,SQSOINDEXB(M,N))/(2d0*DENOM)\n      ENDDO\n      ENDDO\n      if (glu_ij.ne.0) nhel(glu_ij) = back_hel\n      END\n       \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/cpp_process_class.inc" \
    $'  virtual void initProc(string param_card_name); \n\n  // Calculate flavour-independent parts of cross section.\n  virtual void sigmaKin();\n\n  // Evaluate sigmaHat(sHat). \n  virtual double sigmaHat();\n' \
    $'  virtual void initProc(string param_card_name); \n\n  // Calculate flavour-independent parts of cross section.\n  virtual double sigmaKin(double s, double theta);\n\n  // Evaluate sigmaHat(sHat). \n  virtual double sigmaHat();\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/cpp_process_class.inc" \
    $'  virtual int    code()    const {return %(process_code)s;}\n\n  const vector<double>& getMasses() const {return mME;}\n\n  // Get and set momenta for matrix element evaluation\n  vector<double*> getMomenta(){return p;}\n  void setMomenta(vector<double*>& momenta){p = momenta;}\n' \
    $'  virtual int    code()    const {return %(process_code)s;}\n\n  const vector<double>& getMasses() const {return mME;}\n  const vector<double>& getNewMasses() const {return newMasses;}\n  const std::unordered_map<double, double> & getNewDOF() const {return newDOF;}\n  \n  // Get and set momenta for matrix element evaluation\n  vector<double*> getMomenta(){return p;}\n  void setMomenta(vector<double*>& momenta){p = momenta;}\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/cpp_process_class.inc" \
    $'\n  // Pointer to the model parameters\n  Parameters_%(model_name)s* pars;\n\n  // vector with external particle masses\n  vector<double> mME;\n\n' \
    $'\n  // Pointer to the model parameters\n  Parameters_%(model_name)s* pars;\n  \n  // vector with masses of new particles\n  vector<double> newMasses;\n  \n  // dictionary with dof of new particles\n  std::unordered_map<double, double> newDOF;\n  \n  // vector with external particle masses\n  vector<double> mME;\n\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/cpp_process_function_definitions.inc" \
    $'    SLHAReader slha(param_card_name);\n    pars->setIndependentParameters(slha);\n    pars->setIndependentCouplings();\n    pars->printIndependentParameters();\n    pars->printIndependentCouplings();\n    %(initProc_lines)s\n} \n\n//--------------------------------------------------------------------------\n// Evaluate |M|^2, part independent of incoming flavour. \n\nvoid CPPProcess::sigmaKin() { \n    // Set the parameters which change event by event\n    pars->setDependentParameters();\n    pars->setDependentCouplings();\n    static bool firsttime = true;\n    if (firsttime){\n\tpars->printDependentParameters();\n\tpars->printDependentCouplings();\n\tfirsttime = false;\n    }\n\n    // Reset color flows\n    %(reset_jamp_lines)s\n    %(sigmaKin_lines)s\n}\n\n//--------------------------------------------------------------------------\n' \
    $'    SLHAReader slha(param_card_name);\n    pars->setIndependentParameters(slha);\n    pars->setIndependentCouplings();\n    //pars->printIndependentParameters();\n    //pars->printIndependentCouplings();\n    // Set masses and degrees of freedom of new particles\n    newMasses.push_back(pars->mdl_MN1); \n    newDOF[pars->mdl_MN1] = 2.0;\n    newMasses.push_back(pars->mdl_MN2); \n    newDOF[pars->mdl_MN2] = 2.0;\n    newMasses.push_back(pars->mdl_MN3); \n    newDOF[pars->mdl_MN3] = 2.0;\n    newMasses.push_back(pars->mdl_MetR); \n    newDOF[pars->mdl_MetR] = 2.0;\n    newMasses.push_back(pars->mdl_MetI); \n    newDOF[pars->mdl_MetI] = 2.0;\n    newMasses.push_back(pars->mdl_Metp); \n    newDOF[pars->mdl_Metp] = 2.0;\n    %(initProc_lines)s\n} \n\n//--------------------------------------------------------------------------\n// Evaluate |M|^2, part independent of incoming flavour. \n\ndouble CPPProcess::sigmaKin(double s, double theta) { \n    // Set the parameters which change event by event\n    pars->setDependentParameters();\n    pars->setDependentCouplings();\n    static bool firsttime = true;\n    if (firsttime){\n\t//pars->printDependentParameters();\n\t//pars->printDependentCouplings();\n\tfirsttime = false;\n    }\n\n    // Reset color flows\n    %(reset_jamp_lines)s\n    %(sigmaKin_lines)s\n    \n}\n\n//--------------------------------------------------------------------------\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/cpp_process_h.inc" \
    $'\n#include <complex>\n#include <vector>\n%(include_for_complex)s\n\n#include "Parameters_%(model_name)s.h"\n' \
    $'\n#include <complex>\n#include <vector>\n#include <unordered_map>\n%(include_for_complex)s\n\n#include "Parameters_%(model_name)s.h"\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/cpp_process_sigmaKin_function.inc" \
    $'for (int i=0;i < nprocesses; i++)\n    matrix_element[i] /= denominators[i];\n\n\n' \
    $'for (int i=0;i < nprocesses; i++)\n    matrix_element[i] /= denominators[i];\n\nreturn matrix_element[0] * std::sin(theta);\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_goldstone_splitorders_fks.inc" \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n    ANS(:) = 0d0\n    DO M = 1, NAMPSO\n      CF_INDEX = 0 \n      DO I = 1, NCOLOR\n' \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n    DO I = 1, NSQAMPSO\n    ANS(I) = 0d0\n    ENDDO\n    DO M = 1, NAMPSO\n      CF_INDEX = 0 \n      DO I = 1, NCOLOR\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_goldstone_splitorders_fks.inc" \
    $'              ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              ANS(SQSOINDEXSDKG%(ime)d(M,N))=ANS(SQSOINDEXSDKG%(ime)d(M,N))+ZTEMP*DCONJG(JAMP(I,N))\n          ENDDO\n      ENDDO\n    ENDDO\n    ANS(:) = ANS(:)/DENOM\n    END\n       \n       \n' \
    $'              ZTEMP = ZTEMP + CF(CF_INDEX)*JAMP(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              ANS(SQSOINDEXSDKG%(ime)d(M,N))=ANS(SQSOINDEXSDKG%(ime)d(M,N))+ZTEMP*DCONJG(JAMP(I,N))/DENOM\n          ENDDO\n      ENDDO\n    ENDDO\n    END\n       \n       \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_pydispatcher.inc" \
    $'import importlib\nimport sys, os\nimport numpy as np \n\n# update the python path\n' \
    $'import importlib\nimport sys\nimport numpy as np \n\n# update the python path\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_pydispatcher.inc" \
    $'\n# the list of P0* directories\npdir_list = [%(pdir_list)s]\n\ndef import_lib(name):\n    old_dir = os.getcwd()\n    sys.path.insert(0, os.path.join(\'%(path)s\',name))\n    try:\n        os.chdir(os.path.join(\'%(path)s\',name))\n        out = importlib.import_module(\'ewsudpy_%%s\' %% name)\n        os.chdir(old_dir)\n    except:\n        os.chdir(old_dir)\n        sys.path = sys.path[1:]\n        raise\n    return out\n\n\n\n# a dictionary which maps pdgs, in the format ((initial), (sorted final))\n# and the corresponding f2py modules\n' \
    $'\n# the list of P0* directories\npdir_list = [%(pdir_list)s]\n\n# a dictionary which maps pdgs, in the format ((initial), (sorted final))\n# and the corresponding f2py modules\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_pydispatcher.inc" \
    $'    p_transp =np.array([[pp[i] for pp in p] for i in range(4)], order=\'F\')\n    res = np.array([0.,0.,0.,0.,0.,0.], order=\'F\')\n\n    res = pdg2ewsud_dict[pdgs].ewsudakov_py(p_transp,  g)\n\n    return res\n\n' \
    $'    p_transp =np.array([[pp[i] for pp in p] for i in range(4)], order=\'F\')\n    res = np.array([0.,0.,0.,0.,0.,0.], order=\'F\')\n\n    pdg2ewsud_dict[pdgs].ewsudakov_py(p_transp,  g, res)\n\n    return res\n\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_splitorders_fks.inc" \
    $'%(helas_calls1)s\n%(jamp1_lines)s\n\n    ANS(:) = (0d0,0d0)\n\n\nC Reshuffle the momenta here\np_save(:,:) = p(:,:)\n' \
    $'%(helas_calls1)s\n%(jamp1_lines)s\n\n    DO I = 1, NSQAMPSO\n    ANS(I) = (0d0,0d0)\n    ENDDO\n\nC Reshuffle the momenta here\np_save(:,:) = p(:,:)\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/ewsudakov_splitorders_fks.inc" \
    $'          DO J = 1, NCOLOR2\n              ZTEMP = ZTEMP + CF(j,i)*JAMP2(J,M)\n          ENDDO\n      ENDDO\n    ENDDO\n    ANS(:) = ANS(:) /DENOM\nC C NOT NEEDED\nC  include the imaginary factor if needed\nC     if (imag_power.ne.0) ans(:) = ans(:) * imag1**imag_power \n' \
    $'          DO J = 1, NCOLOR2\n              ZTEMP = ZTEMP + CF(j,i)*JAMP2(J,M)\n          ENDDO\n\t  DO N = 1, NAMPSO\n              ANS(SQSOINDEXB(M,N))=ANS(SQSOINDEXB(M,N))+ZTEMP*DCONJG(JAMP1(I,N))/DENOM\n          ENDDO\n      ENDDO\n    ENDDO\nC C NOT NEEDED\nC  include the imaginary factor if needed\nC     if (imag_power.ne.0) ans(:) = ans(:) * imag1**imag_power \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/makefile_sa_f2py" \
    $'PROCESS=  allmatrix.o\nLIBRARY = libmatrix.a\n\nifeq ($(strip $(HERE)),)\n    HERE := ./\nendif\n\n\nPROCNAME= $(notdir $(dir $(abspath $(HERE))))\n\n# For python linking (require f2py part of numpy)\nifeq ($(origin MENUM),undefined)\n  MENUM=2\nendif\n\n#%$(MENUM)py.so: %/matrix.f\n#\t$(F2PY) --f77exec=$(FC) $(LINKLIBS_ME) -c $^ -m $(patsubst %/matrix.f,%$(MENUM)py,$^) --include-paths=$(HERE)/$(patsubst %/matrix.f,%,$^)\n\t\n\t\n#all_matrix$(MENUM)py.so: $(LIBDIR)/$(LIBRARY) all_matrix.f\n#\t$(F2PY) --f77exec=$(FC) $(LINKLIBS_ALL) -c all_matrix.f -m all_matrix$(MENUM)py --include-paths=$(HERE)\n\n    \n#allmatrix$(MENUM)py.so: $(patsubst %/matrix.f,%$(MENUM)py.so,$(wildcard */matrix.f)) all_matrix$(MENUM)py.so\n#\tfor lib in $(patsubst %.so,%,$^); do \\\n#\t\tprintf "try:\\n    from $$lib import *\\nexcept:\\n    from .$$lib import *\\n" >> allmatrix$(MENUM)py.py; \\\n#\tdone\n\t\n\t\n#$(LIBDIR)/$(LIBRARY): $(patsubst %.f,%.o,$(wildcard */matrix.f))  all_matrix.o\n#\t$(call CREATELIB, $@, $^)  \n\n\n$(LIBDIR)/libdhelas.$(dylibext):\n\t$(MAKE) -C "$(LIBDIR)/../Source/DHELAS" shared\n$(LIBDIR)/libmodel.$(dylibext):\n\t$(MAKE) -C "$(LIBDIR)/../Source/MODEL" shared\n\n\nMATRIX_SRCS := $(wildcard */matrix.f)\nMATRIX_OBJS := $(patsubst %.f,%.o,$(wildcard */matrix.f))\n\n%/matrix.o: %/matrix.f\n\t$(MAKE) -C $* matrix.o\n\nliball$(PROCNAME)_$(MENUM)me.$(dylibext): $(LIBDIR)/libdhelas.$(dylibext) $(LIBDIR)/libmodel.$(dylibext) all_matrix.o $(MATRIX_OBJS)\n\t $(FC) $(DYNLIBFLAG) $(RPATHFLAG)liball$(PROCNAME)_$(MENUM)me.$(dylibext) -o liball$(PROCNAME)_$(MENUM)me.$(dylibext) all_matrix.o */matrix.o ../Source/DHELAS/*.o ../Source/MODEL/*.o\n\n\nall_matrix$(MENUM)py.so:  liball$(PROCNAME)_$(MENUM)me.$(dylibext) f2py_wrapper.f makefile\n\tLDFLAGS="-Wl,-rpath,$(HERE)" $(F2PY)  -c f2py_wrapper.f -L$(HERE) -lall$(PROCNAME)_$(MENUM)me $(LINKLIBS) -m                 all_matrix$(MENUM)py\n\ttouch all_matrix$(MENUM)py.so\n' \
    $'PROCESS=  allmatrix.o\nLIBRARY = libmatrix.a\n\n# For python linking (require f2py part of numpy)\nifeq ($(origin MENUM),undefined)\n  MENUM=2\nendif\n\n%$(MENUM)py.so: %/matrix.f\n\t$(F2PY) --f77exec=$(FC) $(LINKLIBS_ME) -c $^ -m $(patsubst %/matrix.f,%$(MENUM)py,$^) --include-paths=$(HERE)/$(patsubst %/matrix.f,%,$^) -I$(HERE)/$(patsubst %/matrix.f,%,$^)\n\t\n\t\nall_matrix$(MENUM)py.so: $(LIBDIR)/$(LIBRARY) all_matrix.f\n\t$(F2PY) --f77exec=$(FC) $(LINKLIBS_ALL) -c all_matrix.f -m all_matrix$(MENUM)py --include-paths=$(HERE) -I$(HERE)\n\n    \nallmatrix$(MENUM)py.so: $(patsubst %/matrix.f,%$(MENUM)py.so,$(wildcard */matrix.f)) all_matrix$(MENUM)py.so\n\tfor lib in $(patsubst %.so,%,$^); do \\\n\t\tprintf "try:\\n    from $$lib import *\\nexcept:\\n    from .$$lib import *\\n" >> allmatrix$(MENUM)py.py; \\\n\tdone\n\t\n\t\n$(LIBDIR)/$(LIBRARY): $(patsubst %.f,%.o,$(wildcard */matrix.f))  all_matrix.o\n\t$(call CREATELIB, $@, $^)  \n\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/makefile_sa_f_sp" \
    $'include ../../Source/make_opts\n\nSHELL = /bin/bash\nHERE := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))\nLIBDIR := $(abspath $(HERE)/../../lib)\nPDIR := $(strip $(notdir $(patsubst %/,%,$(strip $(HERE)))))\nPROG   = check\nPROG_SPLITORDERS = check_sa_born_splitOrders\nLINKLIBS =  -L$(LIBDIR) -ldhelas -lmodel\nLIBS = $(LIBDIR)/libdhelas.$(libext) $(LIBDIR)/libmodel.$(libext)\nLIBS_SHARED = $(LIBDIR)/libdhelas.$(dylibext) $(LIBDIR)/libmodel.$(dylibext)\nPROCESS=  matrix.o\nCHECK_SA=  check_sa.o\nCHECK_SA_SPLITORDERS=  check_sa_born_splitOrders.o\n' \
    $'include ../../Source/make_opts\nSHELL = /bin/bash\nHERE := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))\nLIBDIR = $(HERE)/../../lib/\nPROG   = check\nPROG_SPLITORDERS = check_sa_born_splitOrders\nLINKLIBS =  -L$(LIBDIR) -ldhelas -lmodel\nLIBS = $(LIBDIR)libdhelas.$(libext) $(LIBDIR)libmodel.$(libext)\nPROCESS=  matrix.o\nCHECK_SA=  check_sa.o\nCHECK_SA_SPLITORDERS=  check_sa_born_splitOrders.o\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/makefile_sa_f_sp" \
    $'  MENUM=2\nendif\n\nlibme$(PDIR).$(dylibext): $(LIBDIR)/libdhelas.$(dylibext) $(LIBDIR)/libmodel.$(dylibext) matrix.o\n\tgfortran $(DYNLIBFLAG) -o libme$(PDIR).$(dylibext) matrix.o ../../Source/DHELAS/*.o ../../Source/MODEL/*.o\n\n\n$(LIBDIR)/libdhelas.$(dylibext):\n\t$(MAKE) -C "$(LIBDIR)/../Source/DHELAS" shared\n$(LIBDIR)/libmodel.$(dylibext):\n\t$(MAKE) -C "$(LIBDIR)/../Source/MODEL" shared\n\nmatrix$(MENUM)py.so: f2py_matrix_wrapper.f libme$(PDIR).$(dylibext)  makefile \n\ttouch __init__.py\n\tLDFLAGS="-Wl,-rpath,$(HERE)" $(F2PY)  -c f2py_matrix_wrapper.f -L$(HERE) -lme$(PDIR) $(LINKLIBS) -m matrix$(MENUM)py \n\ttouch matrix$(MENUM)py.so\n\tcp $(LIBDIR)/*$(dylibext) .\n\n\n' \
    $'  MENUM=2\nendif\n\nmatrix$(MENUM)py.so: matrix.f makefile $(LIBS)\n\ttouch __init__.py\n\t$(F2PY) $(LINKLIBS) -c  matrix.f -m matrix$(MENUM)py --f77exec=$(FC) --include-paths=$(HERE) -I$(HERE)\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/matrix_standalone_matchbox_splitOrders_v4.inc" \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n      RES(:) = 0.D0 \n\t  DO M = 1, NAMPSO\n        CF_INDEX = 0\n        DO I = 1, NCOLOR\n' \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n      RES = 0.D0 \n\t  DO M = 1, NAMPSO\n        CF_INDEX = 0\n        DO I = 1, NCOLOR\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/matrix_standalone_matchbox_splitOrders_v4.inc" \
    $'            RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N)) + ZTEMP*DCONJG(JAMP(I,N))\n\t\t  ENDDO\n        ENDDO\n\t  ENDDO\n      RES(:) = RES(:)/DENOM\n      END\n\n      \n' \
    $'            RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N)) + ZTEMP*DCONJG(JAMP(I,N))\n\t\t  ENDDO\n        ENDDO\n\t\tDO N = 1, NAMPSO\n            RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N))/DENOM\n\t\tENDDO\n\t  ENDDO\n\n      END\n\n      \n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/matrix_standalone_splitOrders_v4.inc" \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n      RES(:) = 0.D0 \n\t  DO M = 1, NAMPSO\n        CF_INDEX= 0\n        DO I = 1, NCOLOR\n' \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n      RES = 0.D0 \n\t  DO M = 1, NAMPSO\n        CF_INDEX= 0\n        DO I = 1, NCOLOR\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/matrix_standalone_splitOrders_v4.inc" \
    $'            RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N)) + REAL(ZTEMP*DCONJG(JAMP(I,N)))\n\t\t  ENDDO\n        ENDDO\n\t  ENDDO\n      RES(:) = RES(:)/DENOM\n      END\n\n      SUBROUTINE %(proc_prefix)sGET_value(P, ALPHAS, NHEL ,ANS)\n' \
    $'            RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N)) + REAL(ZTEMP*DCONJG(JAMP(I,N)))\n\t\t  ENDDO\n        ENDDO\n      DO N = 1, NAMPSO\n         RES(%(proc_prefix)sSQSOINDEX(M,N)) = RES(%(proc_prefix)sSQSOINDEX(M,N))/DENOM\n      ENDDO\n\t  ENDDO\n      END\n\n      SUBROUTINE %(proc_prefix)sGET_value(P, ALPHAS, NHEL ,ANS)\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/read_slha.cc" \
    $'  if(!param_card.good())\n    throw "Error while opening param card";\n\n  if(verbose)\n    std::cout << "Opened slha file " << file_name << " for reading" << std::endl;\n  char buf[200];\n  std::string line;\n  std::string block("");\n' \
    $'  if(!param_card.good())\n    throw "Error while opening param card";\n\n  //if(verbose)\n  //  std::cout << "Opened slha file " << file_name << " for reading" << std::endl;\n  char buf[200];\n  std::string line;\n  std::string block("");\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/realmatrix_splitorders_fks.inc" \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n      RES(:) = 0d0\n      DO M = 1, NAMPSO\n      CF_INDEX = 0\n      DO I = 1, NCOLOR\n' \
    $'%(helas_calls)s\n%(jamp_lines)s\n\n      DO I=0,NSQAMPSO\n         RES(I)=0d0\n      ENDDO\n      DO M = 1, NAMPSO\n      CF_INDEX = 0\n      DO I = 1, NCOLOR\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/realmatrix_splitorders_fks.inc" \
    $'          ENDDO\n      ENDDO\n\n      ENDDO\n      RES(:) = RES(:)/DENOM\n      DO I=1,NSQAMPSO\n         RES(0)=RES(0)+RES(I)\n      ENDDO\n' \
    $'          ENDDO\n      ENDDO\n\n\t  DO N = 1, NAMPSO\n            RES(SQSOINDEX%(proc_prefix)s(M,N)) = RES(SQSOINDEX%(proc_prefix)s(M,N))/DENOM \n          ENDDO\n      ENDDO\n\n      DO I=1,NSQAMPSO\n         RES(0)=RES(0)+RES(I)\n      ENDDO\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/super_auto_dsig_group_v4.inc" \
    $'\n    subroutine select_color(rcol, jamp2, iconfig, iproc, icol)\n    implicit none\n    include \'nexternal.inc\'\n    include \'maxamps.inc\' ! for the definition of maxflow\n    include \'coloramps.inc\' ! set the coloramps\n    include \'cluster.inc\'\n    include \'genps.inc\'\n    include \'run.inc\'\nc    \nc   argument IN\nc\n' \
    $'\n    subroutine select_color(rcol, jamp2, iconfig, iproc, icol)\n    implicit none\n    include \'maxamps.inc\' ! for the definition of maxflow\n    include \'coloramps.inc\' ! set the coloramps\nc    \nc   argument IN\nc\n'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

if ! replace_block "$template_dir/super_auto_dsig_group_v4.inc" \
    $'\tinteger i,j\n\tdouble precision xtarget\n\n    if (ickkw.gt.0) then\n        iconfig = igraphs(1)\n    endif   \n\n\n      nc = int(jamp2(0))\n      is_LC = .true.\n      maxcolor=0' \
    $'\tinteger i,j\n\tdouble precision xtarget\n\n      nc = int(jamp2(0))\n      is_LC = .true.\n      maxcolor=0'
then
    rm -rf "$template_dir"
    mv "$original_dir" "$template_dir"
    printf '%s\n' "Failed to modify template_files. The original directory was restored." >&2
    exit 1
fi

# Ensure cpp_process_h.inc ends with exactly one final newline.
cpp_header="$template_dir/cpp_process_h.inc"
cpp_content="$(read_file "$cpp_header")"
cpp_content="${cpp_content%$'\034'}"

while [[ "$cpp_content" == *$'\n' ]]; do
    cpp_content="${cpp_content%$'\n'}"
done

printf '%s\n' "$cpp_content" > "$cpp_header"

printf '%s\n' \
    "template_files modified successfully. Old template_files moved to template_filesOG."

